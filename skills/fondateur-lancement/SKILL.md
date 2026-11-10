---
name: fondateur-lancement
description: >-
  Votre responsable du lancement, pour la Côte d'Ivoire. Construit un plan de
  lancement daté, étape par étape : d'abord un test réel et peu coûteux (liste
  d'attente sur WhatsApp, précommande payée par Mobile Money, stand au marché ou
  dégustation, trois clients pilotes payants), pour que de vrais acheteurs
  confirment ce que le panel simulé a dit ; puis le compte à rebours jusqu'à
  l'ouverture avec responsables et dates limites (formalités, fournisseurs,
  enseigne, comptes, équipe), le déroulé heure par heure du jour J, et les 30
  premiers jours : quoi mesurer et quoi changer. Tient compte des fêtes, des fins
  de mois et de la saison des pluies. À utiliser quand l'utilisateur dit
  « comment je lance », « plan de lancement », « quand est-ce que je peux
  ouvrir », « checklist de lancement », « ouverture » ou « ouverture en douceur ».
argument-hint: "[date de lancement visée]"
---

# fondateur-lancement

Un lancement est un projet avec une date. Ce skill transforme tout le reste du
pack en plan daté, et commence par le moyen le moins cher de savoir si de vraies
personnes paieront, avant que le gros de l'argent ne sorte.

## Étape 1 : tester avant de dépenser

Choisissez le test réel le moins cher qui convient à l'activité, et lancez-le
avant de signer les grosses dépenses de `fondateur/chiffres.json` :

| activité | le test |
| --- | --- |
| commerce physique, restauration | un stand au marché ou à un événement, une dégustation, des précommandes avec un prix et une date de livraison |
| produit en ligne ou livré | un statut WhatsApp et une publication Facebook avec le prix et « je réserve », ou une page de précommande payée par Mobile Money |
| produit numérique | une précommande payée à prix de lancement, avec la date de sortie |
| service | trois clients pilotes payants au prix prévu |
| abonnement | une offre « membres fondateurs » payée d'avance |

Écrivez la ligne de réussite avant de lancer (par exemple : 50 précommandes payées
en deux semaines à 1 000 FCFA), et comparez le résultat au taux d'achat du panel.
Un « je prends » sur WhatsApp n'est pas une vente ; comptez seulement ce qui est
payé ou réservé avec un acompte. Si les vrais acheteurs sont loin derrière le
panel, faites confiance aux vrais acheteurs et revenez à `/fondateur-offre` ou
`/fondateur-prix`.

## Étape 2 : le compte à rebours

D'aujourd'hui au jour du lancement, avec de vraies dates (demandez la date visée ;
sinon prenez la plus proche qui soit réaliste avec les délais de
`fondateur/operations.md`). Des blocs par semaine, chaque tâche avec un
responsable et une date limite :

- Formalités et argent : création au CEPICI, compte bancaire ou comptes
  marchands Mobile Money, autorisations de `fondateur/operations.md`.
- Construction : aménagement ou boutique en ligne, fournisseurs commandés selon
  leurs délais (les importations d'abord).
- Marque : enseigne, emballages, comptes Facebook, TikTok, WhatsApp Business
  depuis `fondateur/marque.md`.
- Marketing : le calendrier de `fondateur/marketing.md` à partir de J-14.
- Équipe : recrutement et formation aux routines.
- Une ouverture en douceur avec la famille, les amis et les voisins avant le
  lancement public.

Vérifiez le calendrier : fêtes religieuses et jours fériés, rentrée scolaire,
fin et début de mois, saison des pluies, grands événements sportifs. Ne lancez
pas un jour où le public sera ailleurs. Marquez le chemin critique : les tâches
qui déplacent la date de lancement si elles glissent.

## Étape 3 : le jour J

Un déroulé heure par heure : qui est où, ce qui part sur quel canal et à quelle
heure, l'offre d'ouverture, qui répond aux messages WhatsApp (ils arrivent en
masse), qui vérifie les paiements Mobile Money avant de livrer, et que faire si
quelque chose casse (d'après le registre des risques : coupure de courant,
réseau en panne, rupture de stock).

## Étape 4 : les 30 premiers jours

Les chiffres à suivre chaque semaine (des finances : unités par jour face au point
d'équilibre ; du marketing : les chiffres de chaque canal ; et le nombre de
clients qui reviennent), le niveau qui déclenche un changement, et un bilan aux
jours 7, 14 et 30 avec les questions à se poser. Demandez aux premiers clients
comment ils vous ont connus et ce qui a failli les faire renoncer.

## Règles

- Français, montants en FCFA, dates en clair (« lundi 2 février »).
- Aucune promesse de date au client qu'un fournisseur n'a pas confirmée.

## Sortie

`fondateur/lancement.md` avec le test, le compte à rebours, le déroulé du jour J et
le bilan des 30 jours. Suite : `/fondateur-plan` assemble tout en plan d'affaires.
