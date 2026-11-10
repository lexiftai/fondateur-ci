#!/usr/bin/env python3
"""Assemble le plan d'affaires pour fondateur-plan. Bibliothèque standard seule, aucun accès réseau.

Lit tout ce que les dix autres skills ont écrit dans fondateur/ et en fait un seul
document, fondateur/plan-d-affaires.md, avec un verdict en tête. Le verdict est
calculé à partir des chiffres, jamais écrit à la main :

    Rentable     chaque vérification qui a des données passe
    Pas encore   au moins une vérification échoue (chaque échec est listé avec son chiffre)
    Incomplet    il n'y a pas encore de chiffres (lancez d'abord fondateur-finances)

Les vérifications :
    1. chaque unité rapporte avant les charges fixes      (fondateur/chiffres.json)
    2. l'année 1 dégage un résultat d'exploitation positif (fondateur/chiffres.json)
    3. le point d'équilibre tient dans la capacité, si une capacité est donnée
    4. assez d'acheteurs du panel achètent               (fondateur/panel/resultats.json, --taux-min, 25% par défaut)

    python3 compiler.py                         # lit ./fondateur, écrit ./fondateur/plan-d-affaires.md
    python3 compiler.py --dir chemin/vers/fondateur --taux-min 0.3
    python3 compiler.py --verifier              # affiche le verdict ; code 0 si Rentable, 1 sinon
"""

import argparse
import importlib.util
import json
import math
import os
import sys

ICI = os.path.dirname(os.path.abspath(__file__))
SECTIONS = [  # (fichier dans fondateur/, titre, skill qui l'écrit)
    ("resume.md", "Résumé", "fondateur-plan"),
    ("conseil.md", "L'avis du conseil", "fondateur-conseil"),
    ("concurrents.md", "La concurrence", "fondateur-concurrents"),
    ("panel/resultats.md", "Le panel d'acheteurs", "fondateur-panel"),
    ("prix.md", "Le prix", "fondateur-prix"),
    ("offre.md", "L'offre", "fondateur-offre"),
    ("finances.md", "Les chiffres", "fondateur-finances"),
    ("marketing.md", "Le marketing", "fondateur-marketing"),
    ("marque.md", "La marque", "fondateur-marque"),
    ("operations.md", "Les opérations", "fondateur-operations"),
    ("lancement.md", "Le plan de lancement", "fondateur-lancement"),
]


def _charger_economie():
    chemin = os.path.join(ICI, "..", "fondateur-finances", "economie_unitaire.py")
    spec = importlib.util.spec_from_file_location("fondateur_economie_unitaire", chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _lire(chemin):
    try:
        with open(chemin, encoding="utf-8") as fh:
            return fh.read().strip()
    except FileNotFoundError:
        return None


def _sans_h1(texte):
    lignes = texte.splitlines()
    if lignes and lignes[0].startswith("# "):
        lignes = lignes[1:]
    # descend les titres d'un niveau pour qu'ils se rangent sous le titre de section
    return "\n".join(("#" + l) if l.startswith("#") else l for l in lignes).strip()


def verdict(d, taux_min=0.25):
    """Rend (verdict, verifications, chiffres, panel). verifications = [(ok, texte)]."""
    verifs = []
    chiffres = panel = None
    eco = _charger_economie()
    brut = _lire(os.path.join(d, "chiffres.json"))
    if brut:
        chiffres = eco.analyser(json.loads(brut))
        u = chiffres["unite"]
        dev = chiffres["devise"]
        c = chiffres["contribution"]
        verifs.append((c > 0, "Chaque %s rapporte %s avant les charges fixes (contribution de %.0f%%)." % (
            u, eco.montant(c, dev), chiffres["contribution_pct"] * 100)
            if c > 0 else "Chaque %s PERD %s avant les charges fixes." % (u, eco.montant(-c, dev))))
        r = chiffres["resultat_an1"]
        verifs.append((r > 0, "Résultat d'exploitation de l'année 1 : %s." % eco.montant(r, dev) if r > 0
                       else "PERTE d'exploitation sur l'année 1 : %s." % eco.montant(-r, dev)))
        eq, cap = chiffres["equilibre_par_jour"], chiffres["capacite_par_jour"]
        if cap is not None:
            tient = not math.isinf(eq) and eq <= float(cap)
            verifs.append((tient, "Le point d'équilibre est %s par jour pour une capacité de %s." % (
                "jamais atteint" if math.isinf(eq) else "de %s %s" % (eco.entier(math.ceil(eq)), eco.pluriel(u)), cap)))
    brut = _lire(os.path.join(d, "panel", "resultats.json"))
    if brut:
        panel = json.loads(brut)
        t = panel["taux_achat"]
        verifs.append((t >= taux_min, "%d acheteurs simulés sur %d achètent (%.0f%%, le seuil est %.0f%%)." % (
            panel["achats"], panel["repondu"], t * 100, taux_min * 100)))
    if chiffres is None:
        v = "Incomplet"
    elif all(ok for ok, _ in verifs):
        v = "Rentable"
    else:
        v = "Pas encore"
    return v, verifs, chiffres, panel


def compiler_plan(d, taux_min=0.25):
    idee = _lire(os.path.join(d, "idee.md"))
    nom = None
    if idee:
        premiere = idee.splitlines()[0]
        nom = premiere[2:].strip() if premiere.startswith("# ") else None
    v, verifs, chiffres, panel = verdict(d, taux_min)
    eco = _charger_economie()
    titre = nom or (chiffres["activite"] if chiffres and chiffres.get("activite") else "Votre activité")
    L = ["# %s · Plan d'affaires" % titre, ""]
    L.append("**Verdict : %s**" % v)
    L.append("")
    for ok, texte in verifs:
        L.append("- %s %s" % ("✓" if ok else "✗", texte))
    if v == "Incomplet":
        L.append("- Pas encore de chiffres. Lancez /fondateur-finances, puis compilez à nouveau.")
    L.append("")
    if chiffres:
        m = lambda x: eco.montant(x, chiffres["devise"])
        u = chiffres["unite"]
        eq = chiffres["equilibre_par_jour"]
        L += ["| chiffre clé | |", "| --- | ---: |",
              "| Prix | %s par %s |" % (m(chiffres["prix"]), u),
              "| Marge nette au volume visé | %.0f%% par %s |" % (chiffres["marge_au_volume_cible"] * 100, u),
              "| Point d'équilibre | %s par jour |" % ("jamais" if math.isinf(eq) else "%s %s" % (eco.entier(math.ceil(eq)), eco.pluriel(u))),
              "| Résultat d'exploitation, année 1 | %s |" % m(chiffres["resultat_an1"]),
              "| Dépenses de démarrage | %s |" % m(chiffres["demarrage"]),
              "| Trésorerie à prévoir avant que l'activité se paie elle-même | %s |" % m(chiffres["tresorerie_a_prevoir"]),
              "| Mise de départ récupérée | %s |" % ("au mois %d" % chiffres["mois_de_retour"] if chiffres["mois_de_retour"] else "pas dans l'année 1")]
        if panel:
            L.append("| Panel d'acheteurs | %d achètent · %d passent |" % (panel["achats"], panel["refus"]))
        L.append("")
    if idee:
        L += ["## L'idée", "", _sans_h1(idee), ""]
    manque = []
    for fichier, titre_s, skill in SECTIONS:
        texte = _lire(os.path.join(d, fichier))
        if texte:
            L += ["## %s" % titre_s, "", _sans_h1(texte), ""]
        else:
            manque.append((titre_s, skill))
    if manque:
        L += ["## Pas encore fait", ""]
        for titre_s, skill in manque:
            L.append("- %s : lancez /%s" % (titre_s, skill))
        L.append("")
    L.append("_Le panel est fait d'acheteurs simulés et les chiffres sont des projections tirées de vos entrées. Confirmez"
             " la demande avec de vrais clients et les coûts avec de vrais devis avant de dépenser. Ce n'est pas un conseil"
             " financier, juridique ni fiscal._")
    return v, "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default="fondateur")
    ap.add_argument("--taux-min", type=float, default=0.25)
    ap.add_argument("--verifier", action="store_true", help="affiche seulement le verdict ; code 0 si Rentable")
    ap.add_argument("--out", help="par défaut : <dir>/plan-d-affaires.md")
    a = ap.parse_args(argv)
    if not os.path.isdir(a.dir):
        print("erreur : pas de dossier %s/ ici. Lancez d'abord les autres skills fondateur." % a.dir, file=sys.stderr)
        return 2
    v, texte = compiler_plan(a.dir, a.taux_min)
    if a.verifier:
        _, verifs, _, _ = verdict(a.dir, a.taux_min)
        print("Verdict : %s" % v)
        for ok, t in verifs:
            print("  %s %s" % ("✓" if ok else "✗", t))
        return 0 if v == "Rentable" else 1
    out = a.out or os.path.join(a.dir, "plan-d-affaires.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(texte)
    print("Verdict : %s. Écrit : %s" % (v, out))
    return 0


if __name__ == "__main__":
    sys.exit(main())
