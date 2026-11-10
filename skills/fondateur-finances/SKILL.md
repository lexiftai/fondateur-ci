---
name: fondateur-finances
description: >-
  Votre directeur financier, en FCFA. Calcule l'économie unitaire d'une activité
  avant de dépenser : ce que rapporte une unité après ses coûts directs (frais
  Mobile Money compris), la vraie marge au volume visé, le point d'équilibre en
  unités par jour, l'année 1 mois par mois, la trésorerie à prévoir avant que
  l'activité se paie elle-même, le mois où la mise de départ est récupérée, et ce
  qui se passe si le prix baisse, si les ventes déçoivent ou si les coûts montent.
  Rappelle ce qu'on oublie en Côte d'Ivoire : son propre salaire, la CNPS, le
  régime fiscal (TEE, RME, RSI, RNI), les coupures d'électricité, les mois creux.
  Chaque nombre remonte à une entrée vérifiable. À utiliser quand l'utilisateur
  dit « calcule mes marges », « fais les chiffres », « est-ce rentable », « point
  mort », « seuil de rentabilité », « combien il me faut pour démarrer », ou
  « lance le directeur financier ».
argument-hint: "[chemin vers chiffres.json]"
---

# fondateur-finances

La personne qui demande « et ça coûte combien ? ». Les marges décident si une
bonne idée est une activité. Ce skill les trouve, chaque nombre relié à une
entrée qu'on peut vérifier.

Outil dans ce dossier :

```bash
python3 "${CLAUDE_SKILL_DIR}/economie_unitaire.py" fondateur/chiffres.json --out fondateur/finances.md
```

## Étape 1 : réunir les entrées

Écrivez `fondateur/chiffres.json` (forme : `exemple.json` dans ce dossier, un
kiosque de jus fictif à Cocody Angré). Il faut :

| champ | ce qu'on y met |
| --- | --- |
| `unite` | ce qu'est une vente : une bouteille, une commande, une séance, un client-mois |
| `devise` | `FCFA` par défaut ; montants entiers, sans centimes |
| `prix` | prix d'une unité, hors taxes |
| `couts_variables` | le coût d'UNE unité : matière, emballage, livraison payée par vous. Avec `cout` (un montant) ou `taux` (une part du prix : `0.01` = 1%) pour les frais d'encaissement Mobile Money, une commission de revendeur ou de plateforme |
| `charges_fixes_mensuelles` | ce qu'on paie chaque mois quoi qu'on vende : loyer, salaires, charges sociales, électricité, internet, et **votre propre salaire** |
| `demarrage` | dépenses uniques avant l'ouverture : caution, aménagement, matériel, premier stock, formalités, lancement |
| `jours_par_mois` | jours de vente réels dans le mois (26 si on ferme le dimanche) |
| `volume_cible_par_jour` | le volume une fois l'activité lancée |
| `montee_par_jour` | 12 nombres : le volume réaliste de chaque mois de l'année 1 |
| `capacite_par_jour` | le plus qu'on peut physiquement vendre en un jour, s'il y a une limite |

D'où viennent les nombres, dans cet ordre :

1. Les devis, factures, baux et listes de prix de l'utilisateur.
2. Des prix publics vérifiables (la grille de frais marchand publiée par
   l'opérateur Mobile Money, l'annonce d'un local, le prix d'un fournisseur).
   Notez la source à côté du nombre dans `fondateur/finances-sources.md`.
3. Votre estimation, marquée comme estimation, avec le raisonnement. Ne
   présentez jamais une estimation comme un fait.

Demandez à l'utilisateur ce que lui seul sait (le loyer qu'on lui a annoncé, les
salaires qu'il versera). Prenez le prix dans `fondateur/prix.md` ou
`fondateur/pitch.md` s'ils existent.

## Ce qu'on oublie souvent en Côte d'Ivoire

Passez cette liste avec l'utilisateur ; ajoutez une ligne pour tout ce qui
s'applique, avec un montant vérifié ou une estimation marquée :

- **Votre propre salaire.** Si l'activité ne vous paie pas, elle n'est pas
  rentable : elle vit de votre travail gratuit. Mettez-le dans les charges fixes.
- **Les salaires et la CNPS.** Pas en dessous du SMIG (75 000 FCFA par mois
  depuis 2023, à revérifier au moment du calcul). Les cotisations sociales
  patronales s'ajoutent au salaire : faites confirmer le taux par la CNPS ou un
  comptable.
- **Les frais d'encaissement.** Chaque opérateur Mobile Money publie ses frais
  marchands ; ils changent. Posez-les en `taux`. Ajoutez les frais de retrait si
  l'argent doit sortir en espèces.
- **L'électricité et les coupures.** Une activité qui dépend du froid ou des
  machines a besoin d'un plan pour les délestages (groupe, carburant, pertes de
  stock).
- **Le transport et la livraison**, y compris les courses que vous faites
  vous-même pour vous approvisionner.
- **La data et le téléphone** : WhatsApp est un outil de travail.
- **Les impôts.** Le régime fiscal dépend du chiffre d'affaires annuel : taxe
  d'État de l'entreprenant (TEE), impôt des microentreprises (RME), réel
  simplifié (RSI), réel normal (RNI). Les seuils et les taux changent avec les
  lois de finances : vérifiez-les sur le site de la DGI ou avec un comptable, et
  ne citez aucun taux que vous n'avez pas lu dans un texte en vigueur. La TVA
  (18% au taux normal) se facture en principe dans les régimes réels et pas dans
  les petits régimes : faites-le confirmer, et dites si les prix doivent l'inclure.
- **Les taxes communales** (enseigne, occupation du domaine public) si
  l'activité a un local ou un étal.

**La montée en charge, c'est là que les plans mentent.** Le premier mois n'est
presque jamais au volume visé. Si le panel a tourné, servez-vous de son taux
d'achat et des achats du premier mois pour vérifier la montée
(`fondateur/panel/resultats.md`), et dites comment. Pensez aussi aux mois creux
et aux mois forts (fin d'année, rentrée, Ramadan, saison des pluies) : la montée
n'a pas à être une ligne droite.

## Étape 2 : lancer l'outil

```bash
python3 "${CLAUDE_SKILL_DIR}/economie_unitaire.py" fondateur/chiffres.json --out fondateur/finances.md
```

Il écrit : le tableau par unité et la contribution (ce que chaque vente laisse
après ses propres coûts), les charges fixes, le point d'équilibre en unités par
jour, la marge nette au volume visé, l'année 1 mois par mois, le résultat
d'exploitation de l'année 1 et le résultat après le démarrage, la trésorerie à
prévoir, le mois où la mise de départ revient, et un tableau « et si » (prix
-10%, volume -20%, coûts unitaires +15%). Il signale un prix sous le coût
variable, un équilibre au-dessus de la capacité, une année 1 en perte et une mise
non récupérée en 12 mois.

« Et si » sans toucher au fichier :

```bash
python3 "${CLAUDE_SKILL_DIR}/economie_unitaire.py" fondateur/chiffres.json --prix 1500
python3 "${CLAUDE_SKILL_DIR}/economie_unitaire.py" fondateur/chiffres.json --volume 0.8
```

## Étape 3 : la note du directeur financier

Ajoutez une courte section en tête de `fondateur/finances.md`, avec des mots
simples :

- **La marge** : la marge nette au volume visé et la contribution par unité.
- **La ligne à surveiller** : le coût ou l'hypothèse qui bouge le plus le
  résultat (souvent la montée en charge, le loyer ou le prix), avec le « et si »
  qui le prouve.
- **La trésorerie** : combien il faut avant que l'activité se paie elle-même, et
  d'où peut venir cet argent (épargne, tontine, famille, microfinance, prêt
  bancaire, structures d'appui aux PME), sans promettre aucun financement.
- **Trois façons d'améliorer la marge**, chacune avec le nombre qu'elle change et
  de combien (lancez le « et si », ne devinez pas).
- Si les conditions du conseil sur l'argent (`fondateur/conseil.md`) sont remplies.

## Règles

- Chaque nombre de votre note vient de la sortie de l'outil ou d'une entrée que
  vous pouvez nommer.
- Le chiffre d'affaires est hors taxes ; dites si le régime de l'utilisateur
  ajoute une taxe.
- Ce n'est pas un conseil financier, fiscal ni juridique. Dites une fois qu'un
  comptable doit vérifier la forme juridique, les charges sociales et le régime
  fiscal avant que l'argent ne bouge.
- Montants en FCFA, « 10 000 FCFA ».

## Sortie

`fondateur/chiffres.json`, `fondateur/finances.md`, `fondateur/finances-sources.md`.
Suite : `/fondateur-plan` utilise ces chiffres pour le verdict ;
`/fondateur-prix` si la marge est mince.
