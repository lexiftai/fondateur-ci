# Fondateur CI

Onze skills Claude pour tester une activité avant de la lancer en Côte d'Ivoire.
En français, montants en FCFA, Mobile Money et WhatsApp compris. Gratuit, licence
MIT, aucun compte ni clé à brancher.

Adaptation de [The Founder skill](https://github.com/Jakeschincariol/founder-skill)
de Jake Schincariol. La méthode d'origine est gardée ; le marché, les exemples,
les chiffres, les formalités et les canaux sont ceux de la Côte d'Ivoire.

## Ce qui change par rapport à l'original

- **Tout en français**, vouvoiement par défaut, montants entiers au format
  « 10 000 FCFA », pourcentages collés (« 34% »).
- **Un quatrième membre au conseil : la lentille Terrain.** Elle juge l'idée sur
  le pouvoir d'achat en fin de mois, la confiance envers un vendeur inconnu, le
  Mobile Money, la distribution par WhatsApp et le bouche-à-oreille, la
  concurrence informelle, la logistique (délestages, adresses, livreurs), les
  saisons et les fêtes, Abidjan face au reste du pays, formel ou informel.
- **Le panel parle ivoirien** : prénoms courants en Côte d'Ivoire, revenu mensuel
  en FCFA, salaire de fin de mois ou rentrées journalières, moyen de paiement
  habituel (Wave, Orange Money, MTN MoMo, Moov Money, espèces). Chaque acheteur dit
  comment il paierait, et le bilan le compte.
- **Les finances** acceptent des frais en pourcentage du prix (`taux`), pour les
  frais Mobile Money ou une commission, et rappellent ce qu'on oublie : son propre
  salaire, la CNPS, le régime fiscal (TEE, RME, RSI, RNI), les délestages.
- **Le prix** propose des prix ronds à tester et tient compte du petit format, du
  moment du mois, du marchandage et du « prix en inbox ».
- **La marque** passe par l'OAPI et l'OIPI, le `.ci`, et vérifie le sens du nom
  dans les langues locales.
- **Les opérations** listent CEPICI, RCCM, DGI, CNPS, mairie, hygiène, ARTCI, et
  la vérification des paiements Mobile Money avant de livrer.
- **L'exemple** n'est plus un café matcha à Toronto mais Jus Lagune, un kiosque
  de jus naturels fictif à Cocody Angré : bouteille de 50 cl à 1 000 FCFA,
  équilibre à 34 bouteilles par jour, marge nette de 34% à 90 bouteilles par jour,
  mise de 1 505 000 FCFA récupérée au mois 6. Ce sont des chiffres d'exemple, à
  remplacer par les vôtres.

## Installer

En Claude Code, copier les dossiers dans vos skills personnels :

```bash
cp -r skills/fondateur-* ~/.claude/skills/
```

ou dans `.claude/skills/` d'un projet pour les limiter à ce projet. Sans Claude
Code, collez un `SKILL.md` en tête d'une conversation : la méthode marche, sans
les sous-agents ni les outils Python.

Les outils demandent Python 3.8 ou plus récent. Rien à installer.

## Les onze

| commande | rôle | ce qu'il fait |
| --- | --- | --- |
| `/fondateur-conseil` | Conseil d'administration | Quatre membres, chacun un sous-agent avec une lentille (Offre, d'après *$100M Offers* ; Monopole, d'après *Zero to One* ; Produit, d'après la biographie de Steve Jobs par Isaacson ; Terrain, le marché ivoirien), notent l'idée, nomment ce qui la tuerait et votent. |
| `/fondateur-concurrents` | Éclaireur de la concurrence | Concurrents directs, indirects et informels, depuis Facebook, TikTok, WhatsApp, Google Maps et les sites, avec prix, positionnement et plaintes de leurs clients, chaque fait avec un lien. |
| `/fondateur-panel` | Panel de consommateurs | 100 acheteurs simulés (20 en `--rapide`) tirés de votre client cible, chacun avec son revenu, son comportement, son objection et son moyen de paiement ; compte qui achète, qui passe et pourquoi. |
| `/fondateur-prix` | Stratège prix | Fourchette de prix acceptable à partir du panel, face aux concurrents et à la marge, prix ronds, échelle de prix et deux prix à tester. |
| `/fondateur-offre` | Architecte de l'offre | Bonus, garantie finançable, preuve et confiance, vraie urgence, nom ; reteste sur le panel. |
| `/fondateur-finances` | Directeur financier | Contribution par vente, marge nette, équilibre par jour, année 1 mois par mois, trésorerie à prévoir, retour sur la mise, « et si ». |
| `/fondateur-marketing` | Directeur marketing | Positionnement, canaux ivoiriens, campagne datée de 30 jours, dix accroches, budget en FCFA, coût maximal d'un client. |
| `/fondateur-marque` | Designer de marque | Noms vérifiés (OAPI, `.ci`, comptes, sens dans les langues locales), voix, promesse, brief visuel. |
| `/fondateur-operations` | Responsable des opérations | Fournisseurs, personnel, routines, outils, formalités, registre des risques ; renvoie les vrais coûts aux finances. |
| `/fondateur-lancement` | Responsable du lancement | Un test réel peu coûteux d'abord, puis compte à rebours daté, jour J heure par heure, 30 premiers jours. |
| `/fondateur-plan` | Rédacteur du plan d'affaires | Assemble tout avec un verdict calculé : Rentable, Pas encore ou Incomplet ; résumé et page unique pour une banque ou un associé. |

## L'ordre

Chacun lit ce que les autres ont écrit, dans un dossier `fondateur/` de votre projet.

```
conseil -> concurrents -> panel -> prix -> offre -> finances -> marketing -> marque -> operations -> lancement -> plan
```

Chacun peut aussi tourner seul. `/fondateur-panel --rapide` sur une idée encore
floue est une bonne façon de savoir s'il faut continuer.

## Les outils

Quatre, en Python standard. Aucun n'accède au réseau.

```bash
python3 skills/fondateur-finances/economie_unitaire.py fondateur/chiffres.json --out fondateur/finances.md
python3 skills/fondateur-panel/panel.py init --client fondateur/client.json --pitch fondateur/pitch.md
python3 skills/fondateur-prix/van_westendorp.py fondateur/panel/reponses --prix 1000
python3 skills/fondateur-plan/compiler.py --dir fondateur
```

```bash
python3 -m unittest discover -s tests -v
```

## Les précautions

**Le conseil applique des cadres publiés. Ce n'est pas ces personnes.** Les
lentilles Offre, Monopole et Produit résument avec nos mots des idées de
*$100M Offers* d'Alex Hormozi, *Zero to One* de Peter Thiel avec Blake Masters, et
la biographie de Steve Jobs par Walter Isaacson. Le conseil ne parle jamais en
leur nom et ne prétend pas qu'ils approuvent quoi que ce soit. La lentille Terrain
n'est attribuée à personne. Ce projet n'a aucun lien avec eux.

**Le panel, ce sont des acheteurs simulés, pas des clients.** Il trouve vite les
objections, les segments et les mots. Ce n'est pas une prévision : les modèles de
langue penchent vers le oui, et ils connaissent moins bien le terrain qu'un vrai
client. Lisez le taux d'achat comme un plafond et confirmez avec de vraies
personnes ; `/fondateur-lancement` commence par là. Une réponse du panel n'est
jamais un témoignage.

**Les chiffres valent ce que valent les entrées.** Les finances marquent chaque
estimation comme telle et demandent de vrais devis. Faites vérifier la forme
juridique, les charges sociales et le régime fiscal par un comptable.

**Les recherches se font sur des sources publiques, avec des liens.** Aucun
concurrent, prix, avis ou citation inventé.

**Ce n'est pas un conseil financier, juridique ni fiscal.** Les formalités, les
taux et les seuils changent ; les skills disent quoi vérifier et où, un
professionnel confirme.

## Licence

MIT. Version d'origine © 2026 Jake Schincariol ; adaptation © 2026 Joel Adou.
Voir `LICENSE`.
