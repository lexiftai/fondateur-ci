---
name: fondateur-offre
description: >-
  Construit une offre difficile à refuser pour un acheteur ivoirien. Liste chaque
  obstacle entre l'acheteur et le résultat qu'il veut (à commencer par la
  méfiance envers un vendeur inconnu, le prix comparé à l'informel et la peur de
  payer sans recevoir), transforme chacun en solution, garde ce qui coûte peu et
  vaut beaucoup, puis empile : bonus honnêtes, garantie que les finances peuvent
  tenir (remboursement, paiement à la livraison, essai), vraie urgence et nom
  clair. Note l'offre sur l'équation de valeur (résultat, probabilité, temps,
  effort) et la reteste sur un panel rapide. À utiliser quand l'utilisateur dit
  « améliore mon offre », « pourquoi les gens n'achètent pas », « qu'est-ce que je
  dois inclure », « garantie », « bonus », « offre irrésistible », ou après un
  panel où beaucoup passent.
argument-hint: "[ce que vous vendez]"
---

# fondateur-offre

La plupart des activités vendent un produit. Les bonnes vendent une offre : le
produit plus tout ce qui rend l'achat facile à accepter. Ce skill la construit,
avec comme méthode la lentille Offre de `../fondateur-conseil/lentilles.md` (un
résumé du cadre de *$100M Offers* d'Alex Hormozi ; ne le présentez jamais comme
ses mots) et la lentille Terrain du même fichier pour les réalités ivoiriennes.

## Étape 1 : lire ce qu'on sait déjà

- `fondateur/idee.md` et `fondateur/pitch.md` : ce qui est vendu aujourd'hui.
- `fondateur/panel/resultats.md` : pourquoi les acheteurs passent, avec leurs
  mots. C'est la matière première : chaque grande objection doit trouver sa
  réponse dans l'offre.
- `fondateur/chiffres.json` : ce que coûte chaque ajout, pour que la pile reste
  rentable.
- `fondateur/conseil.md` : les conditions du conseil.

## Étape 2 : la liste des problèmes

Écrivez chaque obstacle entre l'acheteur et le résultat qu'il veut, avec ses
mots : avant l'achat (doute, prix, effort pour changer d'habitude), pendant
(attente, apprentissage, déplacement), après (est-ce que ça dure, et si ça ne
marche pas). Visez 15 à 30. Partez des objections du panel et des plaintes contre
les concurrents. En Côte d'Ivoire, vérifiez qu'y figurent :

- « Et si je paie et que je ne reçois rien ? »
- « Je ne connais personne qui a déjà acheté chez vous. »
- « La livraison va encore traîner, ou le prix va changer à l'arrivée. »
- « Ce sera moins bien que sur la photo. »
- « C'est trop cher pour maintenant ; je verrai à la fin du mois. »
- « Je n'ai pas Wave » / « je n'ai que du liquide ».

## Étape 3 : solutions, triées et empilées

Transformez chaque problème en solution (une fonction, un service, une garantie,
un format, une façon de payer). Notez chacune sur la valeur pour l'acheteur (1 à
5) et le coût pour la livrer (1 à 5, d'après les chiffres des finances). Gardez
valeur haute et coût bas. Empilez ce qui reste en :

- **Le cœur** : le produit lui-même, décrit par le résultat, pas par les
  ingrédients.
- **Les bonus** : deux ou trois, chacun tue une objection précise.
- **La garantie** : ce qui se passe si ça ne tient pas sa promesse. En Côte
  d'Ivoire, les formes qui rassurent le plus : remboursement simple et rapide par
  Mobile Money, paiement à la livraison, échange sans discussion, premier essai
  offert ou à petit prix. Calculez ce qu'elle coûte à un taux de réclamation
  réaliste avec l'outil des finances avant de la promettre. Le paiement à la
  livraison a un coût caché (commandes refusées à la porte, livreur payé pour
  rien) : chiffrez-le.
- **La preuve** : la confiance compte autant que l'offre. Un visage, une adresse,
  un numéro WhatsApp qui répond, des photos réelles, les premiers clients qui
  acceptent d'en parler (avec leur accord, jamais inventés).
- **L'urgence et la rareté** : seulement si elles sont vraies (une semaine
  d'ouverture, un premier lot limité, une date de rentrée). Jamais de faux compte
  à rebours ni de « plus que 3 en stock ».
- **Le nom** : un nom clair et précis pour l'offre, pas pour l'entreprise.

## Étape 4 : la noter

Sur l'équation de valeur, avant et après, de 1 à 10 chacun : résultat rêvé,
probabilité perçue de l'obtenir, temps avant le résultat, effort et sacrifice.
Dites quel élément de la pile fait bouger quelle note. Dans ce marché, la
probabilité perçue est souvent la note la plus basse : la confiance la fait
monter plus que n'importe quel bonus.

## Étape 5 : la retester

Écrivez la nouvelle offre dans `fondateur/pitch.md` (gardez l'ancienne en
`fondateur/pitch-v1.md`) et lancez `/fondateur-panel --rapide` avec la même
graine. Donnez le taux d'achat avant et après, et les objections qui ont baissé.
Si rien ne bouge, dites-le : le problème vient peut-être du marché ou du prix, pas
de l'offre.

## Règles

- Chaque promesse doit être livrable et finançable ; vérifiez les coûts avec les
  finances.
- Pas de faux avis, faux témoignages, fausse rareté, fausses réductions ni faux
  « vu à la télé ».
- Respectez les règles de protection du consommateur du pays de l'utilisateur
  pour les garanties et les promesses (en Côte d'Ivoire, la loi n°2016-412 du
  15 juin 2016 relative à la consommation, qui prévoit notamment un droit de
  rétractation pour la vente à distance ; promesses de santé et de gains
  surtout). Ce n'est pas un conseil juridique.
- Français, montants en FCFA.

## Sortie

`fondateur/offre.md` (liste des problèmes, la pile, les coûts, les notes de
l'équation de valeur, le résultat du nouveau test) et `fondateur/pitch.md` mis à
jour. Suite : `/fondateur-finances` pour refaire les chiffres avec la pile, puis
`/fondateur-marketing`.
