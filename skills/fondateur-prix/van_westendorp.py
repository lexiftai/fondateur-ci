#!/usr/bin/env python3
"""Sensibilité au prix (Van Westendorp) pour fondateur-prix. Bibliothèque standard seule.

Chaque acheteur du panel répond à quatre questions : à quel prix ce serait trop
bon marché pour avoir confiance, une bonne affaire, cher, et trop cher pour
acheter. Mises ensemble, ces quatre réponses donnent une fourchette de prix
acceptable et le prix qui laisse le moins de monde mécontent.

    python3 van_westendorp.py fondateur/panel/reponses
    python3 van_westendorp.py prix.csv --out fondateur/courbe-prix.md
    python3 van_westendorp.py fondateur/panel/reponses --prix 1000 --json

L'entrée est soit le dossier des réponses du panel (un JSON par acheteur, écrit
par fondateur-panel), soit un CSV avec les colonnes trop_bas, bonne_affaire,
cher, trop_cher (une ligne par personne interrogée ; les autres colonnes sont
ignorées). Une personne à qui il manque un des quatre nombres, ou qui les donne
dans le désordre (trop bas doit être le plus petit, trop cher le plus grand), est
écartée et comptée.

Les quatre points :

    PMC  point de bon marché marginal   en dessous, trop de gens trouvent ça trop bon marché
    PME  point de cherté marginale      au-dessus, trop de gens trouvent ça trop cher
    OPP  prix optimal                   autant de « trop bon marché » que de « trop cher »
    IPP  prix d'indifférence            autant de « bonne affaire » que de « cher »

De PMC à PME : la fourchette acceptable. Les réponses viennent d'acheteurs
simulés : la fourchette sert à choisir quoi TESTER, puis à le tester avec de vrais.
"""

import argparse
import csv
import glob
import json
import math
import os
import re
import sys

CLES = ("trop_bas", "bonne_affaire", "cher", "trop_cher")
CLES_PANEL = ("prix_trop_bas", "prix_bonne_affaire", "prix_cher", "prix_trop_cher")


class ErreurPrix(Exception):
    pass


def montant(v, devise="FCFA"):
    return "n/d" if v is None else "%s %s" % ("{:,.0f}".format(round(v)).replace(",", " "), devise)


def _f(v):
    """Lit « 1 000 », « 1.000 », « 1,000 », « 1000 FCFA » ou « 2,5 » comme on les tape dans un tableur."""
    s = str(v).replace("FCFA", "").replace("F", "")
    for blanc in (" ", " ", " "):
        s = s.replace(blanc, "")
    s = s.strip()
    if re.match(r"^\d{1,3}([.,]\d{3})+$", s):
        s = s.replace(".", "").replace(",", "")
    else:
        s = s.replace(",", ".")
    try:
        x = float(s)
    except (TypeError, ValueError):
        return None
    return x if x > 0 else None


def lire(chemin):
    """Rend (lignes, ecartees) ; chaque ligne vaut (trop_bas, bonne_affaire, cher, trop_cher)."""
    brut = []
    if os.path.isdir(chemin):
        for fp in sorted(glob.glob(os.path.join(chemin, "*.json"))):
            try:
                with open(fp, encoding="utf-8") as fh:
                    a = json.load(fh)
            except (json.JSONDecodeError, UnicodeDecodeError):
                brut.append(None)
                continue
            brut.append(tuple(_f(a.get(k)) for k in CLES_PANEL))
    elif chemin.endswith(".csv"):
        with open(chemin, newline="", encoding="utf-8") as fh:
            echantillon = fh.read(2048)
            fh.seek(0)
            sep = ";" if echantillon.count(";") > echantillon.count(",") else ","
            for r in csv.DictReader(fh, delimiter=sep):
                brut.append(tuple(_f(r.get(k)) for k in CLES))
    else:
        raise ErreurPrix("donnez le dossier des réponses du panel ou un .csv")
    lignes, ecartees = [], 0
    for r in brut:
        if r is None or any(v is None for v in r) or not (r[0] <= r[1] <= r[2] <= r[3]):
            ecartees += 1
            continue
        lignes.append(r)
    return lignes, ecartees


def courbes(lignes, grille):
    n = float(len(lignes))
    tb = [sum(1 for r in lignes if r[0] >= p) / n for p in grille]   # trop bon marché à p (descend)
    ba = [sum(1 for r in lignes if r[1] >= p) / n for p in grille]   # bonne affaire à p (descend)
    ch = [sum(1 for r in lignes if r[2] <= p) / n for p in grille]   # cher à p (monte)
    tc = [sum(1 for r in lignes if r[3] <= p) / n for p in grille]   # trop cher à p (monte)
    return tb, ba, ch, tc


def croisement(grille, descend, monte):
    """Premier prix où la courbe montante rejoint la descendante (interpolation linéaire)."""
    for i in range(1, len(grille)):
        d0 = monte[i - 1] - descend[i - 1]
        d1 = monte[i] - descend[i]
        if d0 <= 0 <= d1 and d1 != d0:
            t = -d0 / (d1 - d0)
            return grille[i - 1] + t * (grille[i] - grille[i - 1])
        if d0 == 0:
            return grille[i - 1]
    return None


def pas_de_prix(v):
    """Le palier de prix rond usuel pour ce niveau de prix (en FCFA)."""
    if v < 1000:
        return 50
    if v < 5000:
        return 100
    if v < 25000:
        return 500
    if v < 100000:
        return 1000
    return 5000


def prix_ronds(v):
    """Les deux prix ronds qui encadrent v : ceux qu'un client lit et paie sans calculer."""
    if v is None:
        return []
    pas = pas_de_prix(v)
    bas = math.floor(v / pas) * pas
    haut = math.ceil(v / pas) * pas
    return sorted({int(bas), int(haut)} - {0})


def analyser(lignes, pas=None):
    if len(lignes) < 5:
        raise ErreurPrix("il faut au moins 5 réponses complètes (reçu %d)" % len(lignes))
    bas = min(r[0] for r in lignes)
    haut = max(r[3] for r in lignes)
    pas = pas or max(1.0, round((haut - bas) / 400))
    grille, p = [], bas
    while p <= haut + 1e-9:
        grille.append(round(p, 4))
        p += pas
    tb, ba, ch, tc = courbes(lignes, grille)
    pas_bon_marche = [1 - v for v in ba]
    pas_cher = [1 - v for v in ch]
    pts = {
        "PMC": croisement(grille, tb, pas_bon_marche),
        "PME": croisement(grille, pas_cher, tc),
        "OPP": croisement(grille, tb, tc),
        "IPP": croisement(grille, ba, ch),
    }
    return {"n": len(lignes), "points": pts, "fourchette": [pts["PMC"], pts["PME"]],
            "prix_ronds_autour_de_opp": prix_ronds(pts["OPP"]),
            "mediane": {k: sorted(r[i] for r in lignes)[len(lignes) // 2] for i, k in enumerate(CLES)}}


def rapport(res, ecartees, prix=None, devise="FCFA"):
    m = lambda v: montant(v, devise)
    p = res["points"]
    L = ["# Sensibilité au prix", "",
         "%d réponses complètes%s. Acheteurs simulés : servez-vous-en pour choisir quoi tester, pas comme dernier mot." % (
             res["n"], (", %d écartées (incomplètes ou dans le désordre)" % ecartees) if ecartees else ""), "",
         "| point | prix | ce que ça veut dire |", "| --- | ---: | --- |",
         "| PMC | %s | en dessous, trop de gens pensent que c'est trop bon marché pour être bon |" % m(p["PMC"]),
         "| OPP | %s | autant de « trop bon marché » que de « trop cher » : le moins de résistance |" % m(p["OPP"]),
         "| IPP | %s | autant de « bonne affaire » que de « cher » |" % m(p["IPP"]),
         "| PME | %s | au-dessus, trop de gens disent que c'est trop cher pour acheter |" % m(p["PME"]), "",
         "**Fourchette acceptable : de %s à %s.**" % (m(p["PMC"]), m(p["PME"])), ""]
    if res["prix_ronds_autour_de_opp"]:
        L.append("Prix ronds à tester autour de l'OPP : %s." % " et ".join(m(v) for v in res["prix_ronds_autour_de_opp"]))
        L.append("")
    md = res["mediane"]
    L.append("Réponses médianes : trop bon marché %s, bonne affaire %s, cher %s, trop cher %s." % (
        m(md["trop_bas"]), m(md["bonne_affaire"]), m(md["cher"]), m(md["trop_cher"])))
    if prix is not None and p["PMC"] is not None and p["PME"] is not None:
        ou = "dans" if p["PMC"] <= prix <= p["PME"] else ("sous" if prix < p["PMC"] else "au-dessus de")
        L += ["", "Votre prix actuel, %s, est **%s** la fourchette acceptable." % (m(prix), ou)]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("source", help="le dossier des réponses du panel, ou un CSV")
    ap.add_argument("--prix", type=float, help="votre prix actuel, pour le placer dans la fourchette")
    ap.add_argument("--devise", default="FCFA")
    ap.add_argument("--out", help="écrire le rapport ici (markdown)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    try:
        lignes, ecartees = lire(a.source)
        res = analyser(lignes)
    except (ErreurPrix, FileNotFoundError) as e:
        print("erreur : %s" % e, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps(dict(res, ecartees=ecartees), indent=1, ensure_ascii=False))
        return 0
    texte = rapport(res, ecartees, a.prix, a.devise)
    if a.out:
        with open(a.out, "w", encoding="utf-8") as fh:
            fh.write(texte)
        print("écrit : %s" % a.out)
    else:
        sys.stdout.write(texte)
    return 0


if __name__ == "__main__":
    sys.exit(main())
