import json
import os
import shutil
import tempfile
import unittest

from _charger import charger, exemple

panel = charger("fondateur-panel", "panel")


def client():
    with open(exemple("fondateur-panel", "client.exemple.json"), encoding="utf-8") as fh:
        return json.load(fh)


class Distribution(unittest.TestCase):
    def test_meme_graine_memes_fiches(self):
        self.assertEqual(panel.distribuer(client(), 100, 7), panel.distribuer(client(), 100, 7))
        self.assertNotEqual(panel.distribuer(client(), 100, 7), panel.distribuer(client(), 100, 8))

    def test_quotas_exacts_et_prenoms_uniques(self):
        fiches = panel.distribuer(client(), 100, 3)
        segs, pay = {}, {}
        for c in fiches:
            segs[c["segment"]] = segs.get(c["segment"], 0) + 1
            pay[c["paiement"]] = pay.get(c["paiement"], 0) + 1
        self.assertEqual(segs, {"Élève ou étudiant": 25, "Employé ou fonctionnaire": 40,
                                "Commerçant ou indépendant": 25, "Cadre": 10})
        self.assertEqual(pay, {"Wave": 35, "Orange Money": 20, "MTN MoMo": 15, "Moov Money": 5, "Espèces": 25})
        self.assertEqual(len({c["nom"] for c in fiches}), 100)
        self.assertEqual(fiches[0]["id"], "P001")
        self.assertEqual(fiches[-1]["id"], "P100")
        for c in fiches:
            seg = next(s for s in client()["segments"] if s["nom"] == c["segment"])
            self.assertTrue(seg["revenu_mensuel"][0] - 500 <= c["revenu_mensuel"] <= seg["revenu_mensuel"][1] + 500)
            self.assertIn(c["objection"], client()["objections"])

    def test_les_prenoms_sont_uniques(self):
        self.assertEqual(len(panel.PRENOMS), len(set(panel.PRENOMS)))
        self.assertGreaterEqual(len(panel.PRENOMS), 100)

    def test_profil_incomplet_refuse(self):
        c = client()
        del c["objections"]
        with self.assertRaises(panel.ErreurPanel):
            panel.distribuer(c)

    def test_paiements_facultatifs(self):
        c = client()
        del c["paiements"]
        fiches = panel.distribuer(c, 10, 1)
        self.assertTrue(all(f["paiement"] == "" for f in fiches))


class Deroule(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        panel.init(self.d, exemple("fondateur-panel", "client.exemple.json"),
                   exemple("fondateur-panel", "pitch.exemple.md"), n=20, graine=5)

    def tearDown(self):
        shutil.rmtree(self.d)

    def repondre(self, pid, achete, code="prix", **extra):
        a = {"id": pid, "achete": achete, "raison_code": code, "raison": "parce que %s" % pid,
             "achats_premier_mois": 4 if achete else 0, "ce_qui_me_ferait_changer": "" if achete else "un prix plus bas",
             "paierait_avec": "Wave" if achete else ""}
        a.update(extra)
        with open(os.path.join(self.d, "reponses", pid + ".json"), "w", encoding="utf-8") as fh:
            json.dump(a, fh, ensure_ascii=False)

    def test_les_consignes_portent_la_fiche_et_le_pitch(self):
        vagues = panel.ecrire_consignes(self.d, vague=10)
        self.assertEqual([len(w) for w in vagues], [10, 10])
        with open(vagues[0][0][1], encoding="utf-8") as fh:
            consigne = fh.read()
        self.assertIn("Jus Lagune", consigne)
        self.assertIn('"id": "P001"', consigne)
        self.assertIn("Ne sois pas complaisant", consigne)
        self.assertIn("FCFA par mois", consigne)
        self.assertIn("Tu paies d'habitude par :", consigne)

    def test_un_acheteur_qui_a_repondu_n_a_pas_de_nouvelle_consigne(self):
        self.repondre("P001", True, "qualite")
        ids = [j[0] for w in panel.ecrire_consignes(self.d) for j in w]
        self.assertNotIn("P001", ids)
        self.assertEqual(len(ids), 19)

    def test_verifier_et_bilan(self):
        for i in range(1, 21):
            pid = "P%03d" % i
            self.repondre(pid, i <= 8, "qualite" if i <= 8 else ("prix" if i <= 15 else "habitude"))
        self.repondre("P020", False, "ambiance")  # un code de raison inconnu
        pbs = dict(panel.verifier(self.d))
        self.assertEqual(list(pbs), ["P020"])
        res = panel.bilan(self.d)
        self.assertEqual((res["achats"], res["refus"], res["repondu"]), (8, 11, 19))
        self.assertEqual(res["pourquoi_non"][0][0], "prix")
        self.assertEqual(res["pourquoi_non"][0][1], 7)
        self.assertEqual(res["ecartes"][0][0], "P020")
        self.assertEqual(res["paiement_des_acheteurs"], [("Wave", 8)])
        texte = panel.resultats_md(res)
        self.assertIn("**8 achètent · 11 passent**", texte)
        self.assertIn("pas des clients", texte)
        self.assertIn("FCFA par mois", texte)
        self.assertIn("4,0 fois", texte)

    def test_enregistrer_range_une_reponse_affichee_et_refuse_le_reste(self):
        reponse = 'Voici ma réponse :\n```json\n{"id": "P002", "achete": false, "raison_code": "prix", "raison": "trop cher"}\n```'
        panel.enregistrer(self.d, "P002", reponse)
        self.assertNotIn("P002", dict(panel.verifier(self.d)))
        with self.assertRaises(panel.ErreurPanel):
            panel.enregistrer(self.d, "P003", '{"id": "P003", "achete": "peut-être", "raison_code": "prix", "raison": "x"}')
        self.assertEqual(dict(panel.verifier(self.d))["P003"], "manquante")
        with self.assertRaises(panel.ErreurPanel):
            panel.enregistrer(self.d, "P999", '{"id": "P999"}')

    def test_bilan_sans_reponse_refuse(self):
        with self.assertRaises(panel.ErreurPanel):
            panel.bilan(self.d)


if __name__ == "__main__":
    unittest.main()
