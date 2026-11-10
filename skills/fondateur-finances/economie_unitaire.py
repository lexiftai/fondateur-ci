#!/usr/bin/env python3
"""Économie unitaire pour fondateur-finances. Bibliothèque standard seule, aucun accès réseau.

Lit un fichier JSON qui décrit l'activité et sort les chiffres qu'un directeur
financier vérifie avant de dépenser le premier franc : ce que rapporte une unité,
la vraie marge au volume prévu, le nombre d'unités par jour pour couvrir les
charges, l'année 1 mois par mois, et le temps pour récupérer la mise de départ.

    python3 economie_unitaire.py fondateur/chiffres.json
    python3 economie_unitaire.py fondateur/chiffres.json --out fondateur/finances.md
    python3 economie_unitaire.py fondateur/chiffres.json --json
    python3 economie_unitaire.py fondateur/chiffres.json --prix 1500 --volume 0.8

Le fichier (voir exemple.json dans ce dossier) :

    activite                  nom, pour le rapport
    unite                     ce qu'on vend à l'unité : "bouteille", "commande", "client-mois"
    devise                    "FCFA" par défaut ; montants entiers, sans centimes
    prix                      prix d'une unité, hors taxes
    couts_variables           [{libelle, cout}] ou [{libelle, taux}] : coût d'UNE unité
                              (matière, emballage, livraison payée par vous...). "taux" est
                              une part du prix : 0.01 = 1% du prix, pour les frais
                              d'encaissement Mobile Money ou une commission
    charges_fixes_mensuelles  [{libelle, cout}] payées chaque mois quoi qu'on vende :
                              loyer, salaires (le vôtre compris), électricité, internet
    demarrage                 [{libelle, cout}] dépenses uniques avant l'ouverture
    jours_par_mois            jours de vente dans le mois (30 par défaut)
    capacite_par_jour         le plus d'unités vendables en un jour (facultatif)
    volume_cible_par_jour     le volume visé une fois l'activité lancée
    montee_par_jour           12 nombres : unités par jour, mois par mois, en année 1
                              (facultatif ; sinon le volume cible tous les mois)

Chaque nombre du rapport vient de ce fichier. Rien n'est cherché ni deviné. Un
champ manquant est signalé, jamais rempli à votre place.

--prix et --volume font un « et si » sans toucher au fichier : --prix remplace le
prix, --volume multiplie tous les volumes (0.8 = 20% de ventes en moins).
"""

import argparse
import json
import math
import sys


class ErreurChiffres(Exception):
    pass


def montant(v, devise="FCFA"):
    """10 000 FCFA : entier, espaces entre les milliers, comme on l'écrit en Côte d'Ivoire."""
    signe = "-" if v < 0 else ""
    return "%s%s %s" % (signe, "{:,.0f}".format(abs(round(v))).replace(",", " "), devise)


def pluriel(u):
    """bouteille -> bouteilles ; client-mois et prix restent tels quels."""
    return u if u[-1:] in "sxz" or "-" in u or " " in u else u + "s"


def entier(v):
    return "{:,.0f}".format(v).replace(",", " ")


def _somme(lignes, champ, prix=None):
    total = 0.0
    for i, it in enumerate(lignes or []):
        if not isinstance(it, dict) or ("cout" not in it and "taux" not in it):
            raise ErreurChiffres("%s[%d] a besoin d'un 'cout' (ou d'un 'taux' pour les coûts variables)" % (champ, i))
        if "taux" in it:
            if prix is None:
                raise ErreurChiffres("%s[%d] : un 'taux' n'a de sens que pour un coût variable" % (champ, i))
            try:
                total += float(it["taux"]) * prix
            except (TypeError, ValueError):
                raise ErreurChiffres("%s[%d].taux n'est pas un nombre : %r" % (champ, i, it["taux"]))
            continue
        try:
            total += float(it["cout"])
        except (TypeError, ValueError):
            raise ErreurChiffres("%s[%d].cout n'est pas un nombre : %r" % (champ, i, it["cout"]))
    return total


def cout_ligne(it, prix):
    return float(it["taux"]) * prix if "taux" in it else float(it["cout"])


def charger(chemin):
    try:
        with open(chemin, encoding="utf-8") as fh:
            return json.load(fh)
    except FileNotFoundError:
        raise ErreurChiffres("fichier introuvable : %s" % chemin)
    except json.JSONDecodeError as e:
        raise ErreurChiffres("%s n'est pas un JSON valide : %s" % (chemin, e))


def analyser(spec, prix=None, volume=1.0):
    """Rend un dict avec chaque nombre du rapport. Fonction pure, facile à tester."""
    if "prix" not in spec and prix is None:
        raise ErreurChiffres("'prix' manque")
    p = float(prix if prix is not None else spec["prix"])
    if p <= 0:
        raise ErreurChiffres("le prix doit être supérieur à zéro")
    jours = float(spec.get("jours_par_mois", 30))
    var = _somme(spec.get("couts_variables"), "couts_variables", prix=p)
    fixes = _somme(spec.get("charges_fixes_mensuelles"), "charges_fixes_mensuelles")
    demarrage = _somme(spec.get("demarrage"), "demarrage")

    if "volume_cible_par_jour" not in spec and "montee_par_jour" not in spec:
        raise ErreurChiffres("donnez 'volume_cible_par_jour' ou 'montee_par_jour' (12 nombres)")
    cible = float(spec.get("volume_cible_par_jour", 0)) * volume
    montee = spec.get("montee_par_jour")
    if montee is None:
        montee = [cible] * 12
    else:
        if len(montee) != 12:
            raise ErreurChiffres("'montee_par_jour' demande 12 nombres, un par mois (reçu %d)" % len(montee))
        montee = [float(v) * volume for v in montee]
    if not cible:
        cible = montee[-1]

    contribution = p - var
    contribution_pct = contribution / p
    equilibre_jour = math.inf if contribution <= 0 else fixes / (contribution * jours)
    unites_mois_cible = cible * jours
    marge_cible = (contribution - (fixes / unites_mois_cible if unites_mois_cible else math.inf)) / p

    mois = []
    cumul = -demarrage
    mois_retour = None
    for m, par_jour in enumerate(montee, start=1):
        unites = par_jour * jours
        ca = unites * p
        cout_var = unites * var
        resultat = ca - cout_var - fixes
        cumul += resultat
        if mois_retour is None and cumul >= 0:
            mois_retour = m
        mois.append({"mois": m, "par_jour": par_jour, "unites": unites, "chiffre_affaires": ca,
                     "variables": cout_var, "fixes": fixes, "resultat": resultat, "cumul": cumul})
    resultat_an = sum(m["resultat"] for m in mois)
    ca_an = sum(m["chiffre_affaires"] for m in mois)
    # la trésorerie à prévoir : le démarrage plus le trou le plus profond creusé par les pertes
    plus_bas = min([-demarrage] + [m["cumul"] for m in mois])
    tresorerie = -plus_bas

    capacite = spec.get("capacite_par_jour")
    u = spec.get("unite", "unité")
    devise = spec.get("devise", "FCFA")
    alertes = []
    if contribution <= 0:
        alertes.append("Chaque %s perd de l'argent avant même le loyer et les salaires : le prix est sous le coût variable." % u)
    if capacite is not None and equilibre_jour > float(capacite):
        alertes.append("L'équilibre demande %.0f %s par jour mais la capacité est de %s." % (equilibre_jour, pluriel(u), capacite))
    if capacite is not None and cible > float(capacite):
        alertes.append("Le volume visé (%.0f par jour) dépasse la capacité (%s)." % (cible, capacite))
    if resultat_an < 0:
        alertes.append("L'année 1 perd de l'argent sur l'exploitation (%s)." % montant(resultat_an, devise))
    if mois_retour is None:
        alertes.append("La mise de départ n'est pas récupérée dans l'année 1.")

    return {
        "activite": spec.get("activite", ""), "unite": u, "devise": devise,
        "prix": p, "variable_par_unite": var, "contribution": contribution,
        "contribution_pct": contribution_pct, "charges_fixes": fixes, "demarrage": demarrage,
        "volume_cible_par_jour": cible, "marge_au_volume_cible": marge_cible, "equilibre_par_jour": equilibre_jour,
        "capacite_par_jour": capacite, "chiffre_affaires_an1": ca_an, "resultat_an1": resultat_an,
        "an1_apres_demarrage": resultat_an - demarrage, "mois_de_retour": mois_retour,
        "tresorerie_a_prevoir": tresorerie, "mois": mois, "alertes": alertes,
        "lignes_variables": spec.get("couts_variables", []), "lignes_fixes": spec.get("charges_fixes_mensuelles", []),
        "lignes_demarrage": spec.get("demarrage", []),
    }


def sensibilite(spec):
    """Les trois « et si » que tout plan doit encaisser."""
    base = analyser(spec)
    lignes = [("Plan de base", base)]
    lignes.append(("Prix -10%", analyser(spec, prix=base["prix"] * 0.9)))
    lignes.append(("Volume -20%", analyser(spec, volume=0.8)))
    pire = json.loads(json.dumps(spec))
    for it in pire.get("couts_variables", []):
        # un frais en taux monte aussi : sinon un fichier tout en taux ne bougerait pas
        cle = "taux" if "taux" in it else "cout"
        it[cle] = float(it[cle]) * 1.15
    lignes.append(("Coûts unitaires +15%", analyser(pire)))
    return lignes


def rapport(spec, a):
    u = a["unite"]
    d = a["devise"]
    m = lambda v: montant(v, d)
    L = []
    L.append("# Économie unitaire : %s" % (a["activite"] or "votre activité"))
    L.append("")
    L.append("Chaque nombre ci-dessous vient du fichier d'entrée. Rien n'est cherché ni deviné.")
    L.append("")
    L.append("## Par %s" % u)
    L.append("")
    L.append("| ligne | par %s |" % u)
    L.append("| --- | ---: |")
    L.append("| Prix | %s |" % m(a["prix"]))
    for it in a["lignes_variables"]:
        lib = it.get("libelle", "coût")
        if "taux" in it:
            lib = "%s (%s%% du prix)" % (lib, ("%g" % (float(it["taux"]) * 100)).replace(".", ","))
        L.append("| %s | -%s |" % (lib, m(cout_ligne(it, a["prix"]))))
    L.append("| **Contribution** (ce que chaque %s laisse pour payer les charges fixes) | **%s** (%.0f%%) |"
             % (u, m(a["contribution"]), a["contribution_pct"] * 100))
    L.append("")
    L.append("## La marge qui compte")
    L.append("")
    L.append("Charges fixes : %s par mois (%s)." % (m(a["charges_fixes"]), ", ".join(
        "%s %s" % (it.get("libelle", "charge"), m(float(it["cout"]))) for it in a["lignes_fixes"]) or "aucune donnée"))
    L.append("")
    eq = a["equilibre_par_jour"]
    L.append("- **Point d'équilibre : %s par jour.** En dessous, vous perdez de l'argent chaque mois." % (
        "jamais (chaque %s perd de l'argent)" % u if math.isinf(eq) else "%s %s" % (entier(math.ceil(eq)), pluriel(u))))
    L.append("- **Marge nette au volume visé** (%s par jour) : **%.0f%%** de chaque vente, après tous les coûts." % (
        entier(a["volume_cible_par_jour"]), a["marge_au_volume_cible"] * 100))
    if a["capacite_par_jour"] is not None:
        L.append("- Capacité : %s par jour." % a["capacite_par_jour"])
    L.append("")
    L.append("## Année 1, mois par mois")
    L.append("")
    L.append("| mois | %s par jour | chiffre d'affaires | résultat | cumul (après %s de démarrage) |" % (pluriel(u), m(a["demarrage"])))
    L.append("| ---: | ---: | ---: | ---: | ---: |")
    for x in a["mois"]:
        L.append("| %d | %s | %s | %s | %s |" % (x["mois"], entier(x["par_jour"]), m(x["chiffre_affaires"]),
                                             m(x["resultat"]), m(x["cumul"])))
    L.append("")
    L.append("- **Résultat d'exploitation de l'année 1 : %s** pour %s de chiffre d'affaires." % (m(a["resultat_an1"]), m(a["chiffre_affaires_an1"])))
    L.append("- Après les %s de démarrage : %s." % (m(a["demarrage"]), m(a["an1_apres_demarrage"])))
    L.append("- Mise de départ récupérée : %s." % ("au mois %d" % a["mois_de_retour"] if a["mois_de_retour"] else "pas dans l'année 1"))
    L.append("- Trésorerie à prévoir avant que l'activité se paie elle-même : **%s**." % m(a["tresorerie_a_prevoir"]))
    L.append("- Le chiffre d'affaires annuel décide du régime fiscal (TEE, RME, RSI ou RNI) : vérifiez les seuils en vigueur auprès de la DGI.")
    L.append("")
    L.append("## Et si")
    L.append("")
    L.append("| scénario | marge au volume visé | équilibre par jour | résultat année 1 |")
    L.append("| --- | ---: | ---: | ---: |")
    for nom, s in sensibilite(spec):
        eq = s["equilibre_par_jour"]
        L.append("| %s | %.0f%% | %s | %s |" % (nom, s["marge_au_volume_cible"] * 100,
                                              "jamais" if math.isinf(eq) else entier(math.ceil(eq)),
                                              m(s["resultat_an1"])))
    L.append("")
    if a["alertes"]:
        L.append("## Signaux d'alerte")
        L.append("")
        for f in a["alertes"]:
            L.append("- %s" % f)
    else:
        L.append("Aucun signal d'alerte dans ces chiffres. Ils ne valent que ce que valent les entrées : vérifiez chaque coût avec un vrai devis.")
    return "\n".join(L) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("chiffres", help="le chiffres.json de l'activité")
    ap.add_argument("--out", help="écrire le rapport ici (markdown)")
    ap.add_argument("--json", action="store_true", help="sortir les chiffres en JSON")
    ap.add_argument("--prix", type=float, help="prix pour un « et si »")
    ap.add_argument("--volume", type=float, default=1.0, help="multiplicateur de volume pour un « et si »")
    args = ap.parse_args(argv)
    try:
        spec = charger(args.chiffres)
        if args.prix is not None:
            spec = dict(spec, prix=args.prix)
        if args.volume != 1.0:
            spec = dict(spec)
            if "volume_cible_par_jour" in spec:
                spec["volume_cible_par_jour"] = float(spec["volume_cible_par_jour"]) * args.volume
            if "montee_par_jour" in spec:
                spec["montee_par_jour"] = [float(v) * args.volume for v in spec["montee_par_jour"]]
        a = analyser(spec)
    except ErreurChiffres as e:
        print("erreur : %s" % e, file=sys.stderr)
        return 2
    if args.json:
        out = {k: v for k, v in a.items() if not k.startswith("lignes_")}
        out["equilibre_par_jour"] = None if math.isinf(out["equilibre_par_jour"]) else out["equilibre_par_jour"]
        print(json.dumps(out, indent=1, ensure_ascii=False))
        return 0
    texte = rapport(spec, a)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(texte)
        print("écrit : %s" % args.out)
    else:
        sys.stdout.write(texte)
    return 0


if __name__ == "__main__":
    sys.exit(main())
