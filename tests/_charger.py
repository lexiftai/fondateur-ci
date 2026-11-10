"""Charge un outil depuis le dossier d'un skill (les noms de dossier ont des tirets)."""

import importlib.util
import os

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKILLS = os.path.join(RACINE, "skills")


def charger(dossier, nom):
    chemin = os.path.join(SKILLS, dossier, nom + ".py")
    spec = importlib.util.spec_from_file_location("fondateur_" + nom, chemin)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def exemple(dossier, nom):
    return os.path.join(SKILLS, dossier, nom)
