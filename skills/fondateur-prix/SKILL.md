---
name: fondateur-prix
description: >-
  Trouve le prix que les acheteurs paieront vraiment, en FCFA. Transforme les
  quatre réponses de prix de chaque acheteur du panel en fourchette de
  sensibilité Van Westendorp (trop bon marché, bonne affaire, cher, trop cher), la
  confronte à ce que les concurrents facturent vraiment (informel compris) et à
  la marge calculée par fondateur-finances, puis recommande un prix rond, une
  échelle de prix (petit format, format standard, formule ou abonnement), une
  offre d'ouverture et deux prix à tester. Tient compte des réalités ivoiriennes :
  budget de fin de mois, petits formats, marchandage, « prix en inbox », frais
  Mobile Money. À utiliser quand l'utilisateur dit « combien je dois vendre »,
  « fixe mon prix », « est-ce que X FCFA c'est trop cher », « stratégie de prix »,
  « quel prix », ou après le panel.
argument-hint: "[prix actuel en FCFA]"
---

# fondateur-prix

Le prix est le levier le plus rapide sur la marge, et celui que les fondateurs
devinent le plus. Ce skill le fixe à partir de trois choses vérifiables : ce que
les acheteurs ont dit, ce que les concurrents facturent, et ce que l'activité
doit gagner.

Outil dans ce dossier :

```bash
python3 "${CLAUDE_SKILL_DIR}/van_westendorp.py" fondateur/panel/reponses --prix 1000 --out fondateur/courbe-prix.md
```

## Étape 1 : ce que les acheteurs ont dit

Si `/fondateur-panel` a tourné, chaque acheteur a répondu à quatre questions de
prix. Lancez l'outil sur `fondateur/panel/reponses` (ou sur un CSV de vraies
réponses avec les colonnes `trop_bas, bonne_affaire, cher, trop_cher`, séparées
par des virgules ou des points-virgules ; de vraies réponses valent toujours
mieux que des simulées : un sondage Google Forms partagé sur WhatsApp suffit). Il
donne :

| point | sens |
| --- | --- |
| PMC | en dessous, trop de gens pensent que c'est trop bon marché pour être bon |
| OPP | le prix qui rencontre le moins de résistance dans un sens comme dans l'autre |
| IPP | autant de gens trouvent ça une bonne affaire que cher |
| PME | au-dessus, trop de gens n'achètent plus du tout |

De PMC à PME : la fourchette acceptable. L'outil propose aussi les deux prix
ronds autour de l'OPP. Si le panel n'a pas tourné, dites-le et proposez
`/fondateur-panel --rapide` d'abord. N'inventez pas de fourchette.

## Étape 2 : ce que facturent les concurrents

À partir de `fondateur/concurrents.md` (ou en cherchant maintenant leurs prix
publics, avec liens) : le prix des solutions les plus proches pour le même
besoin. Notez ce que chaque prix comprend (livraison, quantité, garantie), pour
comparer ce qui est comparable. Un jus en bouteille de 50 cl se compare aux
autres jus en bouteille et au sachet de bissap qu'il remplace, pas à un soda de
33 cl. Si des concurrents affichent « prix en inbox », dites combien, et que
l'utilisateur peut demander lui-même ces prix comme n'importe quel client.

## Étape 3 : ce dont l'activité a besoin

Dans `fondateur/chiffres.json` : le coût variable par unité et le point
d'équilibre. Lancez l'outil des finances à deux ou trois prix candidats pour voir
la marge et l'équilibre à chacun :

```bash
python3 "${CLAUDE_SKILL_DIR}/../fondateur-finances/economie_unitaire.py" fondateur/chiffres.json --prix 1500
```

Les frais Mobile Money posés en `taux` dans `chiffres.json` suivent le prix
automatiquement.

## Ce qui change en Côte d'Ivoire

- **Des prix ronds.** Le client paie en espèces ou tape un montant sur son
  téléphone : 500, 1 000, 2 500, 5 000, 10 000 FCFA se lisent et se paient sans
  calcul. Un prix à 1 137 FCFA crée de la monnaie à rendre et des doutes.
- **Le petit format ouvre le marché.** Quand le revenu tombe par petites sommes,
  une portion, un sachet, une séance ou un mois d'abonnement vendus moins cher
  touchent des acheteurs que le grand format exclut. Proposez-le dans l'échelle
  si les réponses de prix des segments à petit revenu le justifient.
- **Le moment du mois.** Un prix qui passe en début de mois peut bloquer après le
  15. Le paiement en deux ou trois fois, ou une formule réservée aux premiers
  jours du mois, sont des pistes à tester, pas des certitudes.
- **Le marchandage.** Sur certains produits, l'acheteur s'attend à négocier. Si
  c'est le cas, dites-le, et choisissez entre un prix fixe annoncé comme tel
  (« prix unique, pas de discussion ») et une marge de négociation prévue
  d'avance. Ne gonflez pas un prix pour pouvoir le « baisser ».
- **Afficher le prix.** « Prix en inbox » fait perdre des acheteurs qui ne
  demandent pas. Recommandez d'afficher le prix, sauf raison solide.
- **Les frais.** Dites qui paie les frais Mobile Money et la livraison, et
  affichez-le avant le paiement : un prix qui change à la livraison est une des
  plaintes les plus fréquentes.

## Étape 4 : décider

Écrivez `fondateur/prix.md` :

1. **Le prix**, et pourquoi : sa place dans la fourchette acceptable, face aux
   concurrents (informel compris), et la marge qu'il donne (tirée de l'outil, pas
   devinée). Un prix rond.
2. **L'échelle**, si l'activité peut en avoir une : petit format / format
   standard / formule (taille, lot, abonnement, carte de fidélité), avec une
   raison de monter à chaque marche.
3. **L'offre d'ouverture** : un prix ou un bonus de lancement qui n'habitue pas
   les acheteurs à attendre les promos, avec une date de fin.
4. **Ce qu'il faut tester avec de vrais acheteurs** : deux prix dans la fourchette
   et comment les tester (deux statuts WhatsApp à des jours différents, une
   précommande à chaque prix, deux pages de vente, deux ardoises au kiosque).
5. Les trois objections de prix du panel, mot pour mot, pour que le marketing y
   réponde.

## Règles

- Les réponses de prix d'acheteurs simulés désignent quoi tester. Ce ne sont pas
  des preuves.
- Ne jamais fixer un prix sous le coût variable pour « acheter » des clients sans
  le dire, ni sans dire combien de temps les finances le permettent.
- Pas de faux prix barré : aucun « avant 15 000 FCFA » qui n'a jamais été pratiqué.

## Sortie

`fondateur/courbe-prix.md`, `fondateur/prix.md`. Si le prix change, mettez à jour
`fondateur/chiffres.json` et relancez `/fondateur-finances`. Suite : `/fondateur-offre`.
