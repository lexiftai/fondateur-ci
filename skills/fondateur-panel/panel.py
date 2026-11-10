#!/usr/bin/env python3
"""Le panel d'acheteurs de fondateur-panel. Bibliothèque standard seule, aucun accès réseau.

Tient la comptabilité d'un essaim d'acheteurs simulés : distribue une fiche par
acheteur à partir du profil du client cible (revenu mensuel, âge, comportement,
objection, moyen de paiement), écrit une consigne par acheteur pour un sous-agent,
vérifie les réponses et compte qui achète, qui n'achète pas, et pourquoi.

    python3 panel.py init --client fondateur/client.json --pitch fondateur/pitch.md [--n 100] [--graine 7]
    python3 panel.py consignes [--vague 10]   # une consigne par acheteur restant, en vagues
    python3 panel.py verifier                 # réponses manquantes ou cassées
    python3 panel.py enregistrer P003 < reponse.txt   # range le JSON qu'un acheteur a affiché au lieu de l'écrire
    python3 panel.py bilan [--out fondateur/panel/resultats.md]
    python3 panel.py etat

L'état vit dans fondateur/panel/ (--dir pour changer) : panel.json, fiches.json,
consignes/<id>.md, reponses/<id>.json, resultats.md, resultats.json.

L'outil ne répond jamais à la place d'un acheteur. Chaque nombre de resultats.md
est compté dans les fichiers écrits par les sous-agents. Des acheteurs simulés
trouvent vite et pour pas cher les objections et les points faibles. Ce ne sont
pas des clients : confirmez ce qui compte avec de vraies personnes (une précommande,
une liste d'attente sur WhatsApp, une page avec un prix).
"""

import argparse
import json
import os
import random
import sys

# Prénoms courants en Côte d'Ivoire : prénoms akan liés au jour de naissance,
# prénoms mandingues et musulmans, prénoms chrétiens, prénoms d'autres régions.
PRENOMS = [
    "Kouassi", "Akissi", "Kouadio", "Adjoua", "Konan", "Amenan", "Kouakou", "Ahou", "Yao", "Aya",
    "Koffi", "Affoué", "Kouamé", "Amoin", "N'Guessan", "Ahoua", "Brou", "Assiéta", "Kassi", "Amlan",
    "Moussa", "Mariam", "Seydou", "Fatou", "Ibrahim", "Awa", "Bakary", "Salimata", "Mamadou", "Aminata",
    "Lacina", "Karidja", "Drissa", "Nafissatou", "Ousmane", "Rokia", "Abdoulaye", "Assita", "Souleymane", "Djeneba",
    "Adama", "Bintou", "Siaka", "Kadiatou", "Yacouba", "Sita", "Issouf", "Mawa", "Zoumana", "Tenin",
    "Ange", "Christelle", "Serge", "Prisca", "Hervé", "Edwige", "Arsène", "Murielle", "Jean-Marc", "Grâce",
    "Didier", "Esther", "Désiré", "Ruth", "Stéphane", "Larissa", "Yannick", "Josiane", "Franck", "Nadège",
    "Wilfried", "Carine", "Fabrice", "Sandrine", "Cédric", "Laetitia", "Roland", "Bénédicte", "Guy-Roger", "Inès",
    "Emmanuel", "Marie-Laure", "Josué", "Rebecca", "Thierry", "Sylvie", "Junior", "Estelle", "Patrick", "Flora",
    "Zadi", "Gnagne", "Tia", "Lou", "Gbeuly", "Dago", "Séka", "Bléhoué", "Zouzou", "Djédjé",
    "Soro", "Nahoua", "Tiémoko", "Sanata", "Dramane", "Fanta", "Hamed", "Mariétou", "Lassina", "Korotoum",
    "Eric", "Aïcha", "Romuald", "Ella", "Jonathan", "Henriette", "Steve", "Viviane", "Habib", "Odile",
]
RAISONS = ["prix", "habitude", "besoin", "confiance", "qualite", "commodite", "moment", "paiement",
           "livraison", "valeurs", "autre"]
CHAMPS_REPONSE = {"id", "achete", "raison_code", "raison"}
CHAMPS_PRIX = ("prix_trop_bas", "prix_bonne_affaire", "prix_cher", "prix_trop_cher")
VAGUE = 10


class ErreurPanel(Exception):
    pass


def montant(v, devise="FCFA"):
    return "%s %s" % ("{:,.0f}".format(v).replace(",", " "), devise)


# ── distribution ────────────────────────────────────────────────────────────────
def _quotas(elements, n, cle="part"):
    """Répartit n entre les éléments selon leur part, exactement (plus forts restes)."""
    total = sum(float(it.get(cle, 1)) for it in elements) or 1.0
    brut = [n * float(it.get(cle, 1)) / total for it in elements]
    nb = [int(r) for r in brut]
    ordre = sorted(range(len(elements)), key=lambda i: brut[i] - nb[i], reverse=True)
    for i in ordre[: n - sum(nb)]:
        nb[i] += 1
    return nb


def valider_client(c):
    for k in ("activite", "cible", "segments", "comportements", "objections"):
        if k not in c or c[k] in ("", [], None):
            raise ErreurPanel("client.json a besoin de '%s'" % k)
    for s in c["segments"]:
        if "nom" not in s or "revenu_mensuel" not in s or len(s["revenu_mensuel"]) != 2:
            raise ErreurPanel("chaque segment a besoin d'un nom et d'un revenu_mensuel [bas, haut]")
    for b in c["comportements"]:
        if "nom" not in b:
            raise ErreurPanel("chaque comportement a besoin d'un nom")
    for p in c.get("paiements") or []:
        if "nom" not in p:
            raise ErreurPanel("chaque moyen de paiement a besoin d'un nom")


def distribuer(client, n=100, graine=7):
    """Distribue n fiches. Même client + même n + même graine = mêmes fiches, toujours."""
    valider_client(client)
    if n < 1:
        raise ErreurPanel("--n doit valoir au moins 1")
    rng = random.Random(graine)
    age = client.get("age", [20, 45])
    segs = []
    for s, k in zip(client["segments"], _quotas(client["segments"], n)):
        segs += [s] * k
    comps = []
    for b, k in zip(client["comportements"], _quotas(client["comportements"], n)):
        comps += [b] * k
    paiements = client.get("paiements") or []
    pays = []
    for p, k in zip(paiements, _quotas(paiements, n)):
        pays += [p["nom"]] * k
    rng.shuffle(segs)
    rng.shuffle(comps)
    rng.shuffle(pays)
    noms = PRENOMS[:]
    rng.shuffle(noms)
    while len(noms) < n:
        noms += ["%s %d" % (x, len(noms) // len(PRENOMS) + 1) for x in PRENOMS]
    objections = client["objections"]
    habitudes = client.get("habitudes") or []
    fiches = []
    for i in range(n):
        s, b = segs[i], comps[i]
        bas, haut = float(s["revenu_mensuel"][0]), float(s["revenu_mensuel"][1])
        fiches.append({
            "id": "P%03d" % (i + 1),
            "nom": noms[i],
            "age": rng.randint(int(age[0]), int(age[1])),
            "segment": s["nom"],
            "revenu_mensuel": int(round(rng.uniform(bas, haut), -3)),
            "type_de_revenu": s.get("type_de_revenu", ""),
            "comportement": b["nom"],
            "comportement_comment": b.get("comment", ""),
            "objection": objections[rng.randrange(len(objections))],
            "habitude": habitudes[rng.randrange(len(habitudes))] if habitudes else "",
            "paiement": pays[i] if pays else "",
        })
    return fiches


# ── état ────────────────────────────────────────────────────────────────────────
def _chemin(d, *p):
    return os.path.join(d, *p)


def _lire_json(chemin):
    with open(chemin, encoding="utf-8") as fh:
        return json.load(fh)


def _ecrire_json(chemin, obj):
    os.makedirs(os.path.dirname(chemin) or ".", exist_ok=True)
    with open(chemin, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=1, ensure_ascii=False)
        fh.write("\n")


def init(d, chemin_client, chemin_pitch, n=100, graine=None):
    try:
        client = _lire_json(chemin_client)
    except FileNotFoundError:
        raise ErreurPanel("fichier introuvable : %s" % chemin_client)
    try:
        with open(chemin_pitch, encoding="utf-8") as fh:
            pitch = fh.read().strip()
    except FileNotFoundError:
        raise ErreurPanel("fichier introuvable : %s (écrivez d'abord le pitch : ce que vous vendez, le prix, où)" % chemin_pitch)
    if not pitch:
        raise ErreurPanel("le pitch est vide")
    if graine is None:
        graine = random.SystemRandom().randrange(1, 10 ** 6)
    fiches = distribuer(client, n, graine)
    _ecrire_json(_chemin(d, "panel.json"), {"n": n, "graine": graine, "client": client, "pitch": pitch})
    _ecrire_json(_chemin(d, "fiches.json"), fiches)
    os.makedirs(_chemin(d, "consignes"), exist_ok=True)
    os.makedirs(_chemin(d, "reponses"), exist_ok=True)
    return fiches


def charger_etat(d):
    try:
        return _lire_json(_chemin(d, "panel.json")), _lire_json(_chemin(d, "fiches.json"))
    except FileNotFoundError:
        raise ErreurPanel("aucun panel dans %s : lancez d'abord init" % d)


CONSIGNE = """Tu es un acheteur simulé dans un panel de consommateurs. Un entrepreneur veut savoir, avant de dépenser son argent, si des gens comme toi achèteraient vraiment. Ta réponse ne sert que si elle est honnête : la plupart des gens n'achètent pas la plupart des choses, et un « oui » poli fait plus de tort qu'un « non » franc.

=== QUI TU ES ===
{nom}, {age} ans. {segment}. Tu gagnes environ {revenu} par mois{type_de_revenu_ligne}.
Ta façon d'acheter : {comportement}. {comportement_comment}
{habitude_ligne}{paiement_ligne}La première chose qui te vient en tête devant une offre comme celle-ci : « {objection} »
Tu fais partie de ces gens-là : {cible}.
=== FIN ===

=== CE QUI EST PROPOSÉ (tu le découvres pour la première fois, comme un passant ou quelqu'un qui fait défiler son fil) ===
{pitch}
=== FIN ===

Décide comme {nom} le ferait, avec son argent, ses habitudes et ses doutes, pendant une semaine normale du mois. Compte en {devise}, avec ce qu'il te reste à ce moment du mois. Ne sois pas complaisant. N'invente aucun fait sur l'activité au-delà de ce qui est écrit au-dessus.

Crée le fichier {sortie} avec ton outil d'écriture de fichier (ne te contente pas d'afficher la réponse) et mets-y UNIQUEMENT ce JSON, sans balise markdown, rien d'autre :
{{
  "id": "{id}",
  "achete": true ou false,
  "achats_premier_mois": combien de fois tu achèterais le premier mois (0 si tu n'achètes pas),
  "raison_code": un parmi {raisons},
  "raison": "pourquoi, en une ou deux phrases, avec tes mots",
  "objection": "le doute qui pèse le plus pour toi, avec tes mots",
  "ce_qui_me_ferait_changer": "la chose qui te ferait changer d'avis, ou vide",
  "paierait_avec": "le moyen de paiement que tu utiliserais (Wave, Orange Money, MTN MoMo, Moov Money, espèces, carte...), ou vide",
  "prix_trop_bas": le prix en {devise} auquel ce serait trop bon marché pour être de qualité (un nombre),
  "prix_bonne_affaire": le prix en {devise} auquel ce serait une bonne affaire (un nombre),
  "prix_cher": le prix en {devise} auquel ça commence à être cher mais où tu pourrais encore acheter (un nombre),
  "prix_trop_cher": le prix en {devise} auquel tu n'achèterais pas du tout (un nombre)
}}
"""


def ecrire_consignes(d, vague=VAGUE):
    etat, fiches = charger_etat(d)
    cible = etat["client"]["cible"]
    devise = etat["client"].get("devise", "FCFA")
    a_faire = []
    for c in fiches:
        sortie = _chemin(d, "reponses", c["id"] + ".json")
        if _reponse_ok(sortie, c["id"]) is None:
            continue
        texte = CONSIGNE.format(
            pitch=etat["pitch"], cible=cible, sortie=os.path.abspath(sortie),
            revenu=montant(c["revenu_mensuel"], devise),
            type_de_revenu_ligne=(", %s" % c["type_de_revenu"]) if c.get("type_de_revenu") else "",
            habitude_ligne=("Ta journée : %s.\n" % c["habitude"]) if c.get("habitude") else "",
            paiement_ligne=("Tu paies d'habitude par : %s.\n" % c["paiement"]) if c.get("paiement") else "",
            raisons=" / ".join(RAISONS), devise=devise,
            **{k: v for k, v in c.items() if k not in ("revenu_mensuel", "type_de_revenu", "habitude", "paiement")})
        cp = _chemin(d, "consignes", c["id"] + ".md")
        with open(cp, "w", encoding="utf-8") as fh:
            fh.write(texte)
        a_faire.append((c["id"], os.path.abspath(cp)))
    return [a_faire[i:i + vague] for i in range(0, len(a_faire), vague)]


def _reponse_ok(chemin, pid):
    """None si la réponse est bonne, sinon un court problème."""
    if not os.path.exists(chemin):
        return "manquante"
    try:
        a = _lire_json(chemin)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return "JSON invalide"
    manque = CHAMPS_REPONSE - set(a)
    if manque:
        return "manque " + ", ".join(sorted(manque))
    if a.get("id") != pid:
        return "l'id est %r, %s attendu" % (a.get("id"), pid)
    if not isinstance(a.get("achete"), bool):
        return "'achete' doit valoir true ou false"
    if a.get("raison_code") not in RAISONS:
        return "raison_code %r n'est pas parmi %s" % (a.get("raison_code"), ", ".join(RAISONS))
    return None


def enregistrer(d, pid, texte):
    """Range la PROPRE réponse d'un acheteur qui l'a affichée au lieu de l'écrire. Jamais pour répondre à sa place."""
    _, fiches = charger_etat(d)
    if pid not in {c["id"] for c in fiches}:
        raise ErreurPanel("pas d'acheteur %s dans ce panel" % pid)
    debut = texte.find("{")
    if debut < 0:
        raise ErreurPanel("aucun objet JSON dans la réponse")
    try:
        obj, _ = json.JSONDecoder().raw_decode(texte[debut:])
    except json.JSONDecodeError as e:
        raise ErreurPanel("le JSON de la réponse ne se lit pas : %s" % e)
    chemin = _chemin(d, "reponses", pid + ".json")
    _ecrire_json(chemin, obj)
    pb = _reponse_ok(chemin, pid)
    if pb:
        os.remove(chemin)
        raise ErreurPanel("la réponse de %s n'est pas valide (%s) ; relancez plutôt sa consigne" % (pid, pb))
    return chemin


def verifier(d):
    _, fiches = charger_etat(d)
    pbs = []
    for c in fiches:
        p = _reponse_ok(_chemin(d, "reponses", c["id"] + ".json"), c["id"])
        if p:
            pbs.append((c["id"], p))
    return pbs


# ── bilan ───────────────────────────────────────────────────────────────────────
def _taux(lignes):
    return (sum(1 for r in lignes if r["achete"]) / len(lignes)) if lignes else 0.0


def _num(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def bilan(d):
    etat, fiches = charger_etat(d)
    devise = etat["client"].get("devise", "FCFA")
    par_id = {c["id"]: c for c in fiches}
    lignes, ecartes = [], []
    for c in fiches:
        chemin = _chemin(d, "reponses", c["id"] + ".json")
        p = _reponse_ok(chemin, c["id"])
        if p:
            ecartes.append((c["id"], p))
            continue
        a = _lire_json(chemin)
        lignes.append(dict(par_id[c["id"]], **{k: v for k, v in a.items() if k != "id"}, id=c["id"]))
    if not lignes:
        raise ErreurPanel("aucune réponse valide : lancez d'abord les consignes (panel.py consignes)")

    def grouper(cle):
        out = {}
        for r in lignes:
            if r.get(cle):
                out.setdefault(r[cle], []).append(r)
        return sorted(((k, len(v), _taux(v)) for k, v in out.items()), key=lambda t: -t[2])

    # revenus en tiers de la plage distribuée, pour que les tranches veuillent dire la même chose à chaque passage
    revenus = sorted(r["revenu_mensuel"] for r in lignes)
    c1, c2 = revenus[len(revenus) // 3], revenus[2 * len(revenus) // 3]
    for r in lignes:
        r["tranche_revenu"] = ("moins de %s par mois" % montant(c1, devise)) if r["revenu_mensuel"] < c1 else (
            ("%s et plus par mois" % montant(c2, devise)) if r["revenu_mensuel"] >= c2
            else "de %s à %s par mois" % (montant(c1, devise), montant(c2, devise)))

    non = [r for r in lignes if not r["achete"]]
    oui = [r for r in lignes if r["achete"]]

    def raisons(rs):
        out = {}
        for r in rs:
            out.setdefault(r["raison_code"], []).append(r)
        return sorted(((k, v) for k, v in out.items()), key=lambda kv: -len(kv[1]))

    def moyenne(vals):
        vals = [v for v in vals if v is not None]
        return sum(vals) / len(vals) if vals else None

    paiements = {}
    for r in oui:
        p = (r.get("paierait_avec") or "").strip()
        if p:
            paiements[p] = paiements.get(p, 0) + 1

    return {
        "activite": etat["client"]["activite"], "devise": devise, "graine": etat["graine"], "distribues": len(fiches),
        "repondu": len(lignes), "ecartes": ecartes, "achats": len(oui), "refus": len(non),
        "taux_achat": len(oui) / len(lignes),
        "par_segment": grouper("segment"), "par_comportement": grouper("comportement"),
        "par_revenu": grouper("tranche_revenu"), "par_paiement_habituel": grouper("paiement"),
        "pourquoi_non": [(k, len(v), [r["raison"] for r in v[:2]], [r["id"] for r in v[:2]]) for k, v in raisons(non)],
        "pourquoi_oui": [(k, len(v), [r["raison"] for r in v[:2]], [r["id"] for r in v[:2]]) for k, v in raisons(oui)],
        "bascule": [r["ce_qui_me_ferait_changer"] for r in non if (r.get("ce_qui_me_ferait_changer") or "").strip()],
        "paiement_des_acheteurs": sorted(paiements.items(), key=lambda kv: -kv[1]),
        "achats_premier_mois_par_acheteur": moyenne([_num(r.get("achats_premier_mois")) for r in oui]),
        "reponses_prix": sum(1 for r in lignes if all(_num(r.get(k)) is not None for k in CHAMPS_PRIX)),
    }


def resultats_md(res):
    pct = lambda v: "%.0f%%" % (v * 100)
    L = ["# Panel d'acheteurs : %s" % res["activite"], ""]
    L.append("**%d achètent · %d passent** (%s d'achat) sur %d acheteurs simulés. Graine %s : les mêmes fiches peuvent être redistribuées."
             % (res["achats"], res["refus"], pct(res["taux_achat"]), res["repondu"], res["graine"]))
    if res["ecartes"]:
        L.append("")
        L.append("%d acheteurs sur %d n'ont pas de réponse valide et sont écartés : %s." % (
            len(res["ecartes"]), res["distribues"], ", ".join("%s (%s)" % s for s in res["ecartes"][:10])))
    L.append("")
    L.append("Ce sont des acheteurs simulés, pas des clients. Servez-vous-en pour trouver les objections et les"
             " points faibles, puis confirmez les plus importants avec de vraies personnes avant de dépenser.")
    for titre, cle in (("Par segment", "par_segment"), ("Par comportement d'achat", "par_comportement"),
                       ("Par revenu mensuel", "par_revenu"), ("Par moyen de paiement habituel", "par_paiement_habituel")):
        if not res[cle]:
            continue
        L += ["", "## %s" % titre, "", "| groupe | acheteurs | taux d'achat |", "| --- | ---: | ---: |"]
        for k, n, r in res[cle]:
            L.append("| %s | %d | %s%s |" % (k, n, pct(r), "  (mince)" if n < 8 else ""))
    L += ["", "## Pourquoi ils passent", "", "| raison | acheteurs | avec leurs mots |", "| --- | ---: | --- |"]
    for k, n, citations, ids in res["pourquoi_non"]:
        L.append("| %s | %d | %s |" % (k, n, " · ".join("« %s » (%s)" % (q.replace("|", "/"), i) for q, i in zip(citations, ids))))
    L += ["", "## Pourquoi ils achètent", "", "| raison | acheteurs | avec leurs mots |", "| --- | ---: | --- |"]
    for k, n, citations, ids in res["pourquoi_oui"]:
        L.append("| %s | %d | %s |" % (k, n, " · ".join("« %s » (%s)" % (q.replace("|", "/"), i) for q, i in zip(citations, ids))))
    if res["bascule"]:
        L += ["", "## Ce qui ferait basculer un non", ""]
        for f in res["bascule"][:12]:
            L.append("- %s" % f)
    if res["paiement_des_acheteurs"]:
        L += ["", "## Comment les acheteurs paieraient", ""]
        for p, n in res["paiement_des_acheteurs"]:
            L.append("- %s : %d" % (p, n))
    if res["achats_premier_mois_par_acheteur"] is not None:
        L += ["", "Les acheteurs disent qu'ils achèteraient **%s fois** en moyenne le premier mois."
              % ("%.1f" % res["achats_premier_mois_par_acheteur"]).replace(".", ",")]
    if res["reponses_prix"]:
        L += ["", "%d acheteurs ont donné les quatre réponses de prix. Lancez van_westendorp.py de fondateur-prix sur le dossier des réponses." % res["reponses_prix"]]
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default=os.path.join("fondateur", "panel"))
    sub = ap.add_subparsers(dest="cmd", required=True)
    i = sub.add_parser("init")
    i.add_argument("--client", required=True)
    i.add_argument("--pitch", required=True)
    i.add_argument("--n", type=int, default=100)
    i.add_argument("--graine", type=int)
    p = sub.add_parser("consignes")
    p.add_argument("--vague", type=int, default=VAGUE)
    sub.add_parser("verifier")
    sv = sub.add_parser("enregistrer")
    sv.add_argument("id")
    t = sub.add_parser("bilan")
    t.add_argument("--out")
    sub.add_parser("etat")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "init":
            fiches = init(a.dir, a.client, a.pitch, a.n, a.graine)
            st, _ = charger_etat(a.dir)
            print("%d acheteurs distribués (graine %s) dans %s. Suite : panel.py consignes" % (len(fiches), st["graine"], a.dir))
        elif a.cmd == "consignes":
            vagues = ecrire_consignes(a.dir, a.vague)
            n = sum(len(w) for w in vagues)
            if not n:
                print("chaque acheteur a une réponse valide. Suite : panel.py bilan")
            else:
                print("%d consignes en %d vagues de %d au plus. Lancez une vague à la fois :" % (n, len(vagues), a.vague))
                for k, w in enumerate(vagues, 1):
                    print("vague %d : %s" % (k, " ".join("%s=%s" % job for job in w)))
        elif a.cmd == "verifier":
            pbs = verifier(a.dir)
            if not pbs:
                print("toutes les réponses sont là et valides")
            for pid, pb in pbs:
                print("%s : %s" % (pid, pb))
            return 1 if pbs else 0
        elif a.cmd == "enregistrer":
            print("enregistré : %s" % enregistrer(a.dir, a.id, sys.stdin.read()))
        elif a.cmd == "bilan":
            res = bilan(a.dir)
            texte = resultats_md(res)
            out = a.out or _chemin(a.dir, "resultats.md")
            with open(out, "w", encoding="utf-8") as fh:
                fh.write(texte)
            _ecrire_json(_chemin(a.dir, "resultats.json"), res)
            print("%d achètent · %d passent (%.0f%%). Écrit : %s" % (res["achats"], res["refus"], res["taux_achat"] * 100, out))
        elif a.cmd == "etat":
            st, fiches = charger_etat(a.dir)
            pbs = verifier(a.dir)
            print("%d acheteurs distribués (graine %s), %d ont répondu, %d restants" % (len(fiches), st["graine"], len(fiches) - len(pbs), len(pbs)))
    except ErreurPanel as e:
        print("erreur : %s" % e, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
