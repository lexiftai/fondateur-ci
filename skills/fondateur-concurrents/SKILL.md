---
name: fondateur-concurrents
description: >-
  Cartographie les concurrents et le vide qu'ils laissent, sur le marché ivoirien.
  Trouve les concurrents directs, les indirects et les solutions de remplacement
  (y compris l'informel : la vendeuse du quartier, le revendeur Facebook, le
  « fait maison »), à partir de sources publiques uniquement : pages Facebook,
  TikTok, catalogues WhatsApp, Google Maps, sites, places de marché. Relève ce que
  chacun vend, à quel prix, comment il se présente et ce dont ses clients se
  plaignent, chaque fait avec un lien. Se termine par une carte de positionnement
  et le créneau que la nouvelle activité peut prendre. À utiliser quand
  l'utilisateur dit « qui sont mes concurrents », « le marché est-il saturé »,
  « qu'est-ce qui existe déjà », « analyse de la concurrence », « trouve le
  créneau » ou « contre qui je me bats ».
argument-hint: "[commune, ville ou marché]"
---

# fondateur-concurrents

Chaque acheteur règle déjà ce problème d'une façon ou d'une autre. Ce skill
découvre comment, combien il paie et ce qu'il déteste dans la solution actuelle,
pour que la nouvelle activité parte d'un créneau et pas d'une supposition.

## Les règles

- **Sources publiques seulement, chaque fait avec un lien.** Pages et groupes
  Facebook publics, comptes TikTok et Instagram, sites, catalogues WhatsApp
  Business visibles par lien, fiches Google Maps, places de marché en ligne,
  articles de presse. Si une source est inaccessible, dites-le. N'inventez jamais
  un concurrent, un prix, une note ou un avis.
- **Lire, pas aspirer.** Lisez les pages comme une personne le ferait. Respectez
  les conditions de chaque site.
- **Les citations sont mot pour mot**, courtes, avec le lien. Ce sont des
  éléments d'étude, jamais des témoignages.
- Répondez en français, montants en FCFA (« 10 000 FCFA »).

## Ce qui change en Côte d'Ivoire

- **Beaucoup de concurrents n'ont pas de site.** Ils vivent sur Facebook, TikTok,
  WhatsApp et au marché. Cherchez là d'abord.
- **« Prix en inbox ».** Beaucoup de vendeurs n'affichent pas leurs prix. Notez-le
  comme un fait (c'est un signal : l'acheteur doit demander, donc une partie
  abandonne). Pour avoir le prix, proposez à l'utilisateur de le demander lui-même
  comme n'importe quel client, ou de passer au point de vente. Ne demandez rien
  vous-même en vous faisant passer pour un client.
- **L'informel compte comme un concurrent.** La tantie qui vend le même produit
  au coin de la rue, le revendeur qui importe sans marque, le produit fait à la
  maison. Ils sont rarement en ligne : demandez à l'utilisateur ce qu'il voit sur
  le terrain et notez-le comme « observation de l'utilisateur ».
- **Les avis sont dans les commentaires.** Peu d'activités ont des avis Google
  nombreux. Les plaintes se lisent dans les commentaires Facebook et TikTok, les
  groupes de consommateurs et les avis Google quand il y en a.

## Étape 1 : qui est là

À partir de `fondateur/idee.md` (écrivez-le d'abord s'il manque ; voir
`/fondateur-conseil` étape 0) :

| type | ce que ça veut dire | exemple pour un kiosque de jus à Cocody Angré |
| --- | --- | --- |
| Direct | vend la même chose au même acheteur | les autres vendeurs de jus naturels en bouteille à Angré et à la Riviera |
| Indirect | un autre produit pour le même besoin | les sodas et l'eau au supermarché, les maquis qui servent des jus |
| Remplacement | comment l'acheteur s'en sort sans entreprise | le bissap en sachet de la vendeuse du quartier, le jus fait à la maison |

Visez 5 à 10 directs et indirects, plus les principaux remplacements. Pour une
activité locale, cherchez sur la carte et sur Facebook pour la commune exacte.
Pour une activité en ligne, cherchez comme un acheteur le ferait (« formation
<sujet> Abidjan », « <produit> livraison Abidjan », « <produit> pas cher Côte
d'Ivoire »).

## Étape 2 : les faits

Une ligne par concurrent dans `fondateur/concurrents.csv` :

`nom,type,lien,lieu_ou_canal,prix_article_comparable,ce_qu_il_vend,phrase_de_positionnement,moyens_de_paiement,livraison,note,nombre_avis,date_source`

`phrase_de_positionnement` est son propre slogan ou titre, recopié.
`prix_article_comparable` est le prix de l'article le plus proche de ce que vend
la nouvelle activité, avec ce qu'il comprend ; écrivez `prix en inbox` s'il n'est
pas affiché. `moyens_de_paiement` et `livraison` : ce qu'il annonce publiquement
(Wave, Orange Money, paiement à la livraison, livraison gratuite à partir de...).

## Étape 3 : ce que disent leurs clients

Pour les 3 à 5 principaux, lisez les commentaires et les avis (les plaintes
d'abord, puis les « j'aime bien, mais... »). Rangez les plaintes récurrentes en
thèmes avec leur nombre, et une ou deux citations avec lien pour chacun. Marquez
un thème comme mince s'il repose sur moins de trois commentaires. Thèmes fréquents
à guetter : retard de livraison, produit différent de la photo, vendeur qui ne
répond plus après paiement, prix qui change à la livraison, qualité irrégulière.

## Étape 4 : la carte et le créneau

Écrivez `fondateur/concurrents.md` :

1. Le tableau (tiré du CSV), trié du plus direct au moins direct.
2. Fourchette de prix : le plus bas, le médian, le plus haut pour l'article
   comparable, et combien de concurrents cachent leur prix.
3. Une carte de positionnement en texte : deux axes qui comptent pour cet
   acheteur (prix et confiance, qualité et proximité, rapidité et prix...), et
   où se place chaque concurrent.
4. Les plaintes, classées, avec liens.
5. **Le créneau** : ce que personne ne fait bien et que cette activité pourrait
   faire, appuyé sur les preuves. S'il n'y a pas de créneau, dites-le franchement :
   c'est le résultat le plus utile que ce skill puisse donner.
6. La menace : qui pourrait copier la nouvelle activité le plus vite, et comment
   (un vendeur informel copie souvent en quelques semaines).

## Sortie

`fondateur/concurrents.csv`, `fondateur/concurrents.md`. Suite :
`/fondateur-panel` utilise les plaintes pour écrire de vraies objections ;
`/fondateur-prix` utilise la fourchette de prix.
