---
name: fondateur-panel
description: >-
  Le panel de consommateurs, à l'ivoirienne. Lance un essaim de sous-agents
  acheteurs (100 par défaut, --rapide pour 20) tirés du client cible de
  l'utilisateur, chacun avec son revenu mensuel en FCFA, sa façon d'être payé
  (salaire de fin de mois ou rentrées journalières), son âge, son comportement
  d'achat, son objection et son moyen de paiement habituel (Wave, Orange Money,
  MTN MoMo, Moov Money, espèces). Montre à chacun le même pitch et compte qui
  achète, qui n'achète pas et pourquoi : taux d'achat par segment, raisons du
  refus avec leurs mots, ce qui ferait basculer un non, et les réponses de prix
  pour fondateur-prix. À utiliser quand l'utilisateur dit « est-ce que les gens
  achèteraient », « teste sur des clients », « lance le panel », « simule des
  acheteurs », « qui est mon client » ou « valide la demande ».
argument-hint: "[--n 100 | --rapide] [--graine G]"
---

# fondateur-panel

Au lieu de deviner si les gens achèteront, on le demande à cent d'entre eux, chacun un sous-agent qui joue un acheteur précis
tiré de votre client cible. Vous êtes l'animateur. Vous ne répondez jamais à la
place d'un acheteur.

Ce que l'utilisateur a tapé après `/fondateur-panel` : `$ARGUMENTS`

## L'outil

Toute la comptabilité passe par `panel.py` dans le dossier de ce skill :

```bash
python3 "${CLAUDE_SKILL_DIR}/panel.py" <commande>
```

Plus bas, `PANEL` veut dire exactement ça. Si le chemin n'est pas développé,
utilisez le dossier de base que Claude Code a affiché pour ce skill. L'état vit
dans `fondateur/panel/`.

## Étape 1 : le client cible

Écrivez `fondateur/client.json` (forme : `client.exemple.json` dans ce dossier,
un kiosque de jus fictif à Cocody Angré) :

- `activite`, et `cible` : qui est le client, en une ligne précise.
- `devise` : `FCFA` par défaut.
- `segments` : 2 à 4 groupes avec une `part`, un `revenu_mensuel` [bas, haut] en
  FCFA et un `type_de_revenu` (« salaire versé en fin de mois », « rentrées
  journalières qui varient », « argent de poche, irrégulier »). Le moment du mois
  change tout : ne l'oubliez pas.
- `comportements` : 4 à 8 façons d'acheter avec une `part` et une ligne `comment`
  (fidèle à la vendeuse du quartier, commande sur WhatsApp, demande l'avis des
  proches, négocie tout, dépense surtout en début de mois...).
- `objections` : les 4 à 8 doutes que ce type d'acheteur a vraiment (le prix
  comparé à l'informel, la peur de l'arnaque, l'hygiène, les frais de livraison...).
- `habitudes` (facultatif) : des scènes de la vie courante qui rendent l'acheteur
  concret (le gbaka du matin, le maquis de midi, le marché du dimanche).
- `paiements` (facultatif) : les moyens de paiement avec leur `part`. Chaque
  acheteur reçoit le sien.
- `achat` (facultatif) : ce que « acheter » veut dire quand le client n'est pas
  un consommateur, et sur quoi portent les questions de prix. Par exemple, pour
  une plateforme qui se paie à la commission : « ouvrir une boutique et y faire
  passer ses ventes ; les prix portent sur ce que la plateforme retient sur une
  vente de 5 000 FCFA ». Sans ce champ, un vendeur ou une entreprise simulés
  doivent deviner, et leurs réponses de prix deviennent incomparables.

Partez de quelque chose de réel. Utilisez ce que l'utilisateur sait de ses
clients et, si `/fondateur-concurrents` a tourné, les plaintes de
`fondateur/concurrents.md`. Si l'utilisateur a de vraies données (échanges
WhatsApp, commentaires, réponses à un sondage), préférez-les à vos suppositions
et dites quelles parties sont supposées. Montrez le profil à l'utilisateur en
quelques lignes et laissez-le corriger avant de distribuer : un mauvais client
fausse tout le panel.

## Étape 2 : le pitch

Écrivez `fondateur/pitch.md` : ce qu'un acheteur verrait vraiment. Le produit, le
prix en FCFA, où et comment l'avoir, comment payer, la livraison et son prix,
l'offre d'ouverture s'il y en a une. Trois à six lignes simples, sans
superlatifs, rien que l'activité ne peut pas livrer. Chaque acheteur voit
exactement ce texte.

## Étape 3 : distribuer et lancer

```bash
PANEL init --client fondateur/client.json --pitch fondateur/pitch.md --n 100
PANEL consignes
```

Dans les arguments, `--rapide` veut dire `--n 20`, et `--graine G` se passe tel
quel à `init` (pour retester une offre sur les mêmes acheteurs). `init` distribue
les fiches (même graine, mêmes fiches ; la graine est notée).
`consignes` écrit une consigne par acheteur et les liste en vagues de 10. Pour
chaque vague, envoyez UN message avec un appel à l'outil Agent par acheteur de la
vague (l'outil s'appelle Task dans les anciennes versions de Claude Code) :

- `subagent_type` : `general-purpose`
- `description` : `panel <id>`
- `prompt` : `Lis <chemin de la consigne> et suis-la exactement. C'est toute ta consigne.`

Attendez la fin de toute la vague avant la suivante. Claude Code lance environ
10 appels à la fois par défaut : 100 acheteurs font 10 vagues. Après la dernière :

```bash
PANEL verifier      # liste les réponses manquantes ou cassées
PANEL consignes     # réécrit les consignes de ceux-là seulement ; relancez-les une fois
PANEL bilan
```

Si un acheteur a affiché son JSON dans sa réponse au lieu d'écrire le fichier
(ça arrive), rangez sa propre réponse avec `PANEL enregistrer <id>` et la
réponse sur l'entrée standard ; `enregistrer` refuse tout ce qui n'est pas une
réponse valide. Un acheteur qui échoue deux fois est écarté et compté dans les
résultats. N'écrivez jamais une réponse à la place d'un acheteur.

Avant un panel de 100, dites à l'utilisateur que cela fait 100 appels de
sous-agents et proposez `--rapide` (20 acheteurs, `--n 20`) pour un premier
aperçu. Les sous-agents écrivent chacun un fichier dans `fondateur/panel/reponses/` ;
dans le mode de permission par défaut, c'est une validation par fichier :
proposez le mode d'acceptation des modifications (Maj+Tab) pendant le panel.

## Étape 4 : le lire à l'utilisateur

`PANEL bilan` écrit `fondateur/panel/resultats.md` et `resultats.json`. Donnez à
l'utilisateur :

1. Le titre : « 40 achètent · 60 passent » et le taux d'achat.
2. Qui achète et qui n'achète pas : les segments, comportements, tranches de
   revenu et moyens de paiement qui diffèrent le plus.
3. Pourquoi ils passent : les trois premières raisons, avec une citation chacune,
   telle qu'écrite.
4. Ce qui ferait basculer un non : les réponses les plus répétées.
5. Comment les acheteurs paieraient : si un moyen de paiement manque à l'offre,
   dites-le.
6. Une phrase sur ce qu'il faut changer avant de dépenser, et quel skill le fait
   (prix, offre, marketing).

## Limites honnêtes, à dire une fois

Ce sont des acheteurs simulés. Ils sont bons pour faire remonter des objections,
des segments et des mots auxquels on n'avait pas pensé, et mauvais pour prédire
les vraies ventes : les modèles de langue penchent vers le oui, donc le taux
d'achat est un plafond. Ils connaissent aussi moins bien le terrain ivoirien
qu'un vrai client d'Abobo ou de Cocody. Confirmez les grandes décisions avec de
vraies personnes (une liste d'attente sur WhatsApp, une précommande payée par
Mobile Money, un stand au marché avec un prix) avant de signer quoi que ce soit.
Ne présentez jamais une citation du panel comme un témoignage client.

## La consigne que reçoit chaque acheteur

`panel.py` remplit la fiche dans un modèle fixe (voir `CONSIGNE` dans le script) :
qui est l'acheteur (prénom courant en Côte d'Ivoire, âge, segment, revenu
mensuel et sa régularité, façon d'acheter, une habitude, son moyen de paiement,
le doute qui lui vient), le pitch mot pour mot, l'instruction de ne pas être
complaisant, de compter avec ce qui lui reste à ce moment du mois et de ne rien
inventer, et le JSON exact à écrire : achète ou non, achats le premier mois, un
code de raison, la raison avec ses mots, son objection principale, ce qui le
ferait changer d'avis, comment il paierait, et quatre réponses de prix (trop bon
marché, bonne affaire, cher, trop cher). Ne modifiez jamais la consigne d'un seul
acheteur.

## Sortie

`fondateur/client.json`, `fondateur/pitch.md`, `fondateur/panel/` (fiches,
consignes, réponses, résultats). Suite : `/fondateur-prix` lit les réponses de
prix, `/fondateur-offre` et `/fondateur-marketing` lisent les objections.
