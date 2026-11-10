import json
import os
import re
import unittest

from _charger import RACINE, SKILLS

NOMS = ["fondateur-conseil", "fondateur-concurrents", "fondateur-panel", "fondateur-prix", "fondateur-offre",
        "fondateur-finances", "fondateur-marketing", "fondateur-marque", "fondateur-operations",
        "fondateur-lancement", "fondateur-plan"]
CADRATIN = chr(0x2014)  # construit en code pour que ce fichier ne se signale pas lui-même
ANCIENS = ("founder/", "/founder-", "numbers.json", "Toronto", "matcha", "USPTO")


def entete(chemin):
    with open(chemin, encoding="utf-8") as fh:
        texte = fh.read()
    m = re.match(r"^---\n(.*?)\n---\n", texte, re.S)
    return (m.group(1) if m else ""), texte


def fichiers_texte():
    for base, dossiers, fichiers in os.walk(RACINE):
        dossiers[:] = [d for d in dossiers if d not in (".git", "__pycache__", "fondateur")]
        for f in fichiers:
            if f.endswith((".md", ".py", ".json", ".txt")) or f in ("LICENSE", "LICENCE", ".gitignore"):
                yield os.path.join(base, f)


class Depot(unittest.TestCase):
    def test_onze_dossiers(self):
        trouves = sorted(d for d in os.listdir(SKILLS) if os.path.isfile(os.path.join(SKILLS, d, "SKILL.md")))
        self.assertEqual(trouves, sorted(NOMS))

    def test_entete_nom_et_description(self):
        for s in NOMS:
            fm, texte = entete(os.path.join(SKILLS, s, "SKILL.md"))
            self.assertIn("name: %s\n" % s, fm + "\n", s)
            self.assertRegex(fm, r"description: ", s)
            self.assertGreater(len(fm), 300, "%s : description trop mince" % s)
            self.assertLess(len(fm), 1500, "%s : description trop longue" % s)
            self.assertGreater(len(texte.splitlines()), 60, s)

    def test_les_outils_cites_existent(self):
        for s in NOMS:
            _, texte = entete(os.path.join(SKILLS, s, "SKILL.md"))
            for outil in re.findall(r"\$\{CLAUDE_SKILL_DIR\}/([\w.\-/]+\.(?:py|md))", texte):
                self.assertTrue(os.path.exists(os.path.normpath(os.path.join(SKILLS, s, outil))), "%s : %s" % (s, outil))

    def test_les_skills_cites_existent(self):
        for s in NOMS:
            _, texte = entete(os.path.join(SKILLS, s, "SKILL.md"))
            for cite in re.findall(r"/(fondateur-[a-z]+)", texte):
                self.assertIn(cite, NOMS, "%s cite /%s" % (s, cite))

    def test_chaque_skill_porte_la_licence(self):
        for s in NOMS:
            self.assertTrue(os.path.isfile(os.path.join(SKILLS, s, "LICENCE")), s)
        with open(os.path.join(RACINE, "LICENSE"), encoding="utf-8") as fh:
            self.assertIn("Jake Schincariol", fh.read())

    def test_les_exemples_se_lisent(self):
        for rel in ("fondateur-finances/exemple.json", "fondateur-panel/client.exemple.json"):
            with open(os.path.join(SKILLS, rel), encoding="utf-8") as fh:
                json.load(fh)
        for rel in ("plugin.json", "marketplace.json"):
            with open(os.path.join(RACINE, ".claude-plugin", rel), encoding="utf-8") as fh:
                self.assertEqual(json.load(fh)["name"], "fondateur-ci")

    def test_le_readme_cite_chaque_commande(self):
        with open(os.path.join(RACINE, "README.md"), encoding="utf-8") as fh:
            readme = fh.read()
        for s in NOMS:
            self.assertIn("`/%s`" % s, readme)

    def test_pas_de_tiret_cadratin(self):
        for chemin in fichiers_texte():
            with open(chemin, encoding="utf-8") as fh:
                self.assertNotIn(CADRATIN, fh.read(), os.path.relpath(chemin, RACINE))

    def test_plus_de_reste_de_l_original(self):
        for s in NOMS:
            for chemin in fichiers_texte():
                if not chemin.startswith(os.path.join(SKILLS, s)):
                    continue
                with open(chemin, encoding="utf-8") as fh:
                    texte = fh.read()
                for ancien in ANCIENS:
                    self.assertNotIn(ancien, texte, "%s : %s" % (os.path.relpath(chemin, RACINE), ancien))


if __name__ == "__main__":
    unittest.main()
