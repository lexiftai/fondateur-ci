---
name: fondateur-operations
description: >-
  Votre responsable des opérations, en Côte d'Ivoire. Détermine comment
  l'activité tourne vraiment dès le premier jour : fournisseurs (marchés de gros,
  importateurs, artisans) et leurs prix, délais et conditions, qui travaille
  quand (SMIG, CNPS), les routines d'ouverture, de service ou de livraison et de
  fermeture, les outils (encaissement Mobile Money, WhatsApp Business, caisse,
  comptabilité, livraison), les formalités à vérifier (CEPICI, RCCM, impôts,
  CNPS, mairie, hygiène), et un registre des risques avec un plan pour chacun
  (coupure d'électricité, rupture d'approvisionnement, réseau Mobile Money en
  panne, livreur absent). Renvoie les vrais coûts aux finances. À utiliser quand
  l'utilisateur dit « comment je fais tourner ça », « opérations »,
  « fournisseurs », « personnel », « procédures », « qu'est-ce qu'il me faut pour
  ouvrir », « papiers » ou « premier jour ».
argument-hint: "[commune, ville ou pays]"
---

# fondateur-operations

Un plan qui tient sur le papier échoue un lundi à 7 h, quand le fournisseur n'est
pas venu et que le courant est coupé. Ce skill vérifie que le premier jour, la
première semaine et le premier mois peuvent vraiment être tenus, et que les
chiffres des finances comprennent ce que ça coûte vraiment.

## Étape 1 : ce que l'activité fait chaque jour

À partir de `fondateur/idee.md`, `fondateur/offre.md` et `fondateur/chiffres.json`,
écrivez le cycle d'une journée, étape par étape, du premier geste au dernier
(pour un kiosque de jus : achat des fruits au marché, préparation, mise au frais,
ouverture, vente, réponses WhatsApp, livraisons, nettoyage, comptes de la
journée, commande du lendemain ; pour une boutique en ligne : messages et
commandes, confirmation du paiement, préparation, remise au livreur, suivi,
retours, service client). Marquez les étapes que le client voit.

## Étape 2 : les fournisseurs

Pour chaque entrée des coûts variables et chaque équipement : deux ou trois vrais
fournisseurs que l'utilisateur peut contacter (marché de gros, grossiste,
importateur, artisan, fabricant local), leurs prix publics ou comment obtenir un
devis, les minimums de commande, les délais et les conditions de paiement
(comptant, Mobile Money, crédit fournisseur). Mettez les liens quand il y en a ;
beaucoup de fournisseurs n'ont qu'un numéro WhatsApp ou une adresse au marché :
notez-le comme tel. Là où seul un devis tranchera, dites-le et ajoutez-le aux
questions ouvertes. Pour un produit importé, comptez le transport, le
dédouanement et le délai réel, et gardez une solution locale de secours. Si un
vrai prix diffère de `fondateur/chiffres.json`, mettez à jour le fichier et dites
que les finances doivent être relancées.

## Étape 3 : les personnes

Qui fait quoi, et quand : un planning de la semaine au volume visé et pour le
premier mois, plus calme. Les rôles, les heures et la base de salaire (donnée par
l'utilisateur, ou une source publique pour le SMIG et les salaires courants, avec
lien). Le SMIG est de 75 000 FCFA par mois depuis 2023 ; revérifiez-le. Un
salarié se déclare à la CNPS et les cotisations patronales s'ajoutent : signalez-les
pour le comptable. Dites aussi ce que l'utilisateur fera lui-même, et combien
d'heures ça représente.

## Étape 4 : les routines

Des routines courtes et numérotées pour les moments qui font ou défont
l'activité : l'ouverture, le service ou la livraison, la confirmation d'un
paiement Mobile Money (vérifier la réception sur le compte marchand avant de
livrer, jamais sur une simple capture d'écran envoyée par le client), le
traitement d'une plainte, la fermeture et les comptes, la commande de la semaine.
Chacune tient sur une page qu'une personne pourrait suivre dès son premier jour.

## Étape 5 : les outils

La plus petite pile qui suffit : encaissement (compte marchand Wave, Orange Money,
MTN MoMo, Moov Money, terminal de carte si utile), WhatsApp Business (catalogue,
réponses rapides, étiquettes), caisse ou cahier de ventes, comptabilité simple
(un tableur suffit au début), stock, livraison (livreurs à moto indépendants ou
services de livraison actifs dans la ville). Pour un produit numérique
(formation, eBook, modèle), une plateforme qui encaisse le Mobile Money et livre
automatiquement (Ficsell, par exemple) évite d'envoyer chaque fichier à la main.
De vrais produits, leurs prix publiés, et pourquoi chacun. Pas d'outil payant si
un outil gratuit fait l'affaire au début.

## Étape 6 : formalités, autorisations et assurance

Une liste de ce qu'une activité de ce type demande en général dans la commune ou
le pays de l'utilisateur, chaque point avec la page officielle pour le
confirmer. En Côte d'Ivoire, au minimum :

- **Création** : statut d'entreprenant ou entreprise individuelle ou société
  (SARL, SAS...), au guichet unique du CEPICI (cepici.gouv.ci), qui regroupe
  l'immatriculation au RCCM et la déclaration fiscale d'existence. Ne citez ni
  coût ni délai que vous n'avez pas lus sur le site officiel.
- **Impôts** : le régime fiscal (TEE, RME, RSI, RNI) selon le chiffre d'affaires,
  et les déclarations en ligne sur le portail de la DGI (dgi.gouv.ci).
- **Personnel** : immatriculation de l'employeur et déclaration des salariés à
  la CNPS (cnps.ci).
- **Commune** : autorisation et taxe d'enseigne, occupation du domaine public
  pour un étal ou une terrasse.
- **Hygiène**, pour l'alimentation et la beauté : autorisations sanitaires et
  visites médicales du personnel, à vérifier auprès des services d'hygiène.
- **Données personnelles** : déclaration auprès de l'ARTCI si l'activité
  constitue un fichier de clients.
- **Assurance** : local, stock, responsabilité civile.

Dites clairement que les règles diffèrent selon le lieu et changent, et que
l'utilisateur doit confirmer chaque point auprès de l'administration ou d'un
professionnel. Ce n'est pas un conseil juridique.

## Étape 7 : le registre des risques

Les dix choses les plus susceptibles de mal tourner, chacune avec sa probabilité,
sa gravité et le plan. Pensez au moins à : coupure d'électricité ou d'eau, réseau
Mobile Money ou internet en panne, fournisseur en rupture ou prix qui flambe,
livreur absent ou client injoignable à la livraison, faux paiement (capture
d'écran trafiquée), personne clé malade, mauvais avis ou rumeur sur les réseaux,
vol ou casse, saison des pluies (routes, affluence), mois creux.

## Sortie

`fondateur/operations.md`, et `fondateur/chiffres.json` mis à jour si les vrais
coûts ont changé. Suite : `/fondateur-lancement`.
