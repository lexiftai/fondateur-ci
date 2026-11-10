---
name: fondateur-plan
description: >-
  Votre rédacteur de plan d'affaires. Assemble tout ce que les autres skills
  fondateur ont écrit (l'avis du conseil, les concurrents, le panel d'acheteurs,
  le prix, l'offre, les chiffres des finances, le marketing, la marque, les
  opérations et le lancement) en un seul plan d'affaires en français, avec en tête
  un verdict calculé à partir des chiffres, jamais écrit à la main : Rentable, Pas
  encore (avec les chiffres qui échouent) ou Incomplet. Ajoute un résumé et une
  version d'une page pour un associé, une banque, une microfinance, une structure
  d'appui aux PME ou un investisseur. À utiliser quand l'utilisateur dit « écris
  mon business plan », « fais mon plan d'affaires », « rassemble tout », « est-ce
  rentable », « donne-moi le plan », ou à la fin du pack fondateur.
argument-hint: "[--taux-min 0.25]"
---

# fondateur-plan

La dernière étape. Un document sur lequel l'entrepreneur peut agir, ou qu'il peut
remettre à un associé, à sa banque, à une microfinance ou à un programme d'appui,
construit uniquement à partir de ce que le pack a trouvé.

Outil dans ce dossier :

```bash
python3 "${CLAUDE_SKILL_DIR}/compiler.py" --dir fondateur
```

## Étape 1 : voir ce qui existe

```bash
python3 "${CLAUDE_SKILL_DIR}/compiler.py" --dir fondateur --verifier
```

affiche le verdict et chaque vérification. Les vérifications, toutes calculées :

1. Chaque unité rapporte avant les charges fixes (`fondateur/chiffres.json`).
2. L'année 1 dégage un résultat d'exploitation positif.
3. Le point d'équilibre tient dans la capacité, si une capacité est donnée.
4. Assez d'acheteurs simulés achètent (`fondateur/panel/resultats.json` ; seuil
   par défaut 25%, à changer avec `--taux-min` en disant pourquoi).

Sans chiffres, le verdict est Incomplet : proposez `/fondateur-finances`. Listez
les autres sections manquantes avec le skill qui remplit chacune. Ne remplissez
jamais vous-même une section manquante avec des suppositions.

## Étape 2 : le résumé

Écrivez `fondateur/resume.md`, une demi-page, des mots simples :

- Ce qu'est l'activité et pour qui, en deux phrases.
- Le verdict et les trois chiffres qui le portent (marge, point d'équilibre,
  année 1), en FCFA.
- Ce sur quoi le panel et le conseil sont d'accord, et où ils divergent.
- Le plus gros risque et ce qui sera fait.
- Ce qu'il faut pour démarrer (la trésorerie des finances, le premier test du
  lancement) et d'où l'argent peut venir.
- La seule chose à faire cette semaine.

Si le verdict est Pas encore, le résumé commence par ce qui doit changer et quel
skill le change. N'adoucissez jamais une vérification qui échoue.

## Étape 3 : assembler

```bash
python3 "${CLAUDE_SKILL_DIR}/compiler.py" --dir fondateur
```

écrit `fondateur/plan-d-affaires.md` : titre, verdict et vérifications, tableau des
chiffres clés, l'idée, puis chaque section produite par le pack (résumé, conseil,
concurrence, panel, prix, offre, chiffres, marketing, marque, opérations,
lancement), et ce qui n'est pas encore fait.

## Étape 4 : la page unique

Écrivez `fondateur/une-page.md` pour quelqu'un qui décide en deux minutes : le
problème, le client, l'offre et le prix, le tableau des chiffres, les preuves
(résultat du panel, créneau face aux concurrents, test réel s'il y en a eu), à
quoi servira l'argent, et la demande (montant en FCFA, forme : prêt, apport,
partenariat). Mêmes chiffres que le plan, mot pour mot. Une banque ou une
microfinance demandera souvent aussi les pièces de l'entreprise (RCCM,
déclaration fiscale) et un historique de ventes : dites lesquels manquent.

## Règles

- Le verdict vient de `compiler.py`. N'écrivez jamais Rentable à la main, et
  n'arrondissez jamais un chiffre qui échoue en chiffre qui passe.
- Dites une fois, clairement : le panel est fait d'acheteurs simulés et les
  chiffres sont des projections ; de vrais clients et de vrais devis les
  confirment. Ce n'est pas un conseil financier, juridique ni fiscal.
- Si l'utilisateur veut un PDF ou une présentation, proposez d'exporter le plan,
  mais gardez le markdown comme source.
- Français, montants en FCFA.

## Sortie

`fondateur/resume.md`, `fondateur/plan-d-affaires.md`, `fondateur/une-page.md`.
Donnez ensuite à l'utilisateur le verdict en une ligne et la seule chose à faire
cette semaine.
