---
name: fondateur-conseil
description: >-
  Votre conseil d'administration, pensé pour la Côte d'Ivoire. Met une idée
  d'activité devant quatre membres, chacun un sous-agent qui la lit avec une seule
  lentille : Offre (d'après $100M Offers d'Alex Hormozi), Monopole (d'après Zero
  to One de Peter Thiel), Produit (d'après la biographie de Steve Jobs par Walter
  Isaacson) et Terrain (les réalités du marché ivoirien : pouvoir d'achat en fin de
  mois, confiance, Mobile Money, WhatsApp, concurrence informelle, logistique).
  Chacun note l'idée, nomme ce qui la tuerait et vote : financer, financer sous
  conditions, ou passer. À utiliser quand l'utilisateur dit « teste mon idée »,
  « est-ce que ça peut marcher », « est-ce un bon business », « challenge mon
  projet », « qu'en dirait un investisseur », ou commence le pack fondateur sur une
  nouvelle idée.
argument-hint: "<l'idée d'activité, ou vide pour la prendre dans la conversation>"
---

# fondateur-conseil

La première réunion. Avant de louer un local, d'imprimer une enseigne ou de
lancer une page Facebook, quatre membres du conseil démontent l'idée, chacun sous
un angle différent, et votent.

Ce que l'utilisateur a tapé après `/fondateur-conseil` : `$ARGUMENTS`. Si c'est
vide, prenez l'idée dans la conversation.

## Langue et ton, pour tout le pack

- Écrivez en français. Vouvoyez l'entrepreneur, sauf s'il vous tutoie.
- Montants entiers en FCFA, espaces entre les milliers : « 10 000 FCFA ». Pas de
  centimes. Si l'activité vise un autre pays, utilisez sa devise et dites-le.
- Pourcentages collés : « 34% ».
- Pas de tiret cadratin, pas de formules creuses. Des phrases qu'un commerçant
  d'Adjamé comme une cadre du Plateau comprennent du premier coup.

## La règle sur les trois noms

Les lentilles Offre, Monopole et Produit résument des **cadres publiés**, rien de
plus. Les membres du conseil ne sont pas ces personnes, ne parlent jamais en leur
nom, ne les citent jamais, ne prétendent jamais qu'elles approuveraient quoi que
ce soit. Écrivez « la lentille Offre », jamais « Alex Hormozi dit ». Si
l'utilisateur demande ce que l'un d'eux penserait vraiment, répondez que vous ne
pouvez qu'appliquer leurs cadres publics. La lentille Terrain n'est attribuée à
personne.

## Étape 0 : la fiche idée

Tout le pack lit `fondateur/idee.md` dans le projet de l'utilisateur. Si le
fichier n'existe pas, écrivez-le maintenant à partir de la conversation :

```markdown
# <nom de l'activité, ou un nom provisoire>

- Ce que c'est : une phrase.
- Pour qui : le client cible, aussi précis que l'utilisateur peut l'être (âge,
  quartier ou ville, revenu, habitudes).
- Ce qui est vendu, à quel prix : le produit ou service principal et son prix en FCFA.
- Où et comment : commune ou ville (Cocody, Yopougon, Bouaké...) ou en ligne ;
  comment les clients le trouvent ; comment c'est livré ; comment ils paient
  (Mobile Money, espèces, carte).
- Budget et contraintes : argent disponible (épargne, tontine, famille, prêt),
  temps, compétences, ce qui est déjà décidé.
```

S'il manque le nom, le client, le produit ou le prix, posez la question (trois
questions au plus, en un seul message), puis écrivez le fichier. N'inventez ni
budget, ni taille de marché, ni concurrent.

## Étape 1 : préparer le dossier du conseil

Écrivez `fondateur/conseil/dossier.md` : la fiche idée plus tout ce que
l'utilisateur a dit et qu'un inconnu devrait savoir. **Les sous-agents ne voient
pas cette conversation** : le dossier doit se suffire à lui-même. N'y mettez pas
votre propre avis sur l'idée.

## Étape 2 : réunir le conseil

Lancez quatre sous-agents dans UN SEUL message (outil Agent, `subagent_type:
general-purpose`, un par membre), chacun avec cette consigne : `Lis
fondateur/conseil/dossier.md et le fichier lentilles.md de fondateur-conseil
(chemin ci-dessous), applique UNIQUEMENT la lentille <lentille>, écris ta note en
français dans fondateur/conseil/<lentille>.md.` Le fichier des lentilles est
`lentilles.md` dans le dossier de ce skill (`${CLAUDE_SKILL_DIR}/lentilles.md` ;
si ce chemin n'est pas développé, utilisez le dossier de base que Claude Code a
affiché pour ce skill). Les quatre lentilles : `offre`, `monopole`, `produit`,
`terrain`.

Chaque note, sous cette forme :

```markdown
# Lentille <nom>
Note : <1 à 10> | Vote : FINANCER / FINANCER SI / PASSER
## Ce qui est solide
## Ce qui la tuerait (les 3 premiers risques, le plus dangereux d'abord)
## Les questions que je poserais au fondateur
## Si FINANCER SI : les conditions
```

## Étape 3 : la synthèse du président

Lisez les quatre notes (elles sont courtes) et écrivez `fondateur/conseil.md` :

1. Le vote, par exemple « 2 financer si, 1 financer, 1 passer », et la note moyenne.
2. Les risques soulevés par plus d'un membre : ils passent en premier.
3. Toutes les conditions, fusionnées, en liste à cocher que le reste du pack
   pourra cocher (les finances, le panel et le prix en testeront la plupart).
4. Un paragraphe : la version la plus forte de cette activité que le conseil voit.
   Elle peut différer de ce que l'utilisateur a présenté ; dites-le franchement.

Gardez les désaccords. Un conseil qui est d'accord sur tout n'a pas fait son
travail. Si la lentille Terrain contredit les trois autres, dites pourquoi :
c'est souvent là que se cache le vrai risque.

## Règles

- Notez l'activité, pas la personne.
- Aucun fait inventé. Si une lentille a besoin d'un chiffre que personne n'a
  encore (taille du marché, coût pour gagner un client), notez-le comme question
  ouverte et dites quel skill y répond (`/fondateur-concurrents`,
  `/fondateur-panel`, `/fondateur-finances`).
- Un PASSER est un résultat, pas un échec. Dites-le simplement.

## Sortie

`fondateur/idee.md`, `fondateur/conseil/` (dossier et quatre notes),
`fondateur/conseil.md`. Donnez ensuite le vote en une ligne et proposez la suite :
`/fondateur-concurrents` pour voir qui est déjà là, ou `/fondateur-panel` pour
mettre l'idée devant 100 acheteurs simulés.

## La suite du pack

```
conseil -> concurrents -> panel -> prix -> offre -> finances -> marketing -> marque -> operations -> lancement -> plan
```

Chaque skill peut aussi tourner seul ; chacun lit ce qui existe déjà dans `fondateur/`.
