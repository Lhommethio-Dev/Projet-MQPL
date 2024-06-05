import unittest
from datetime import datetime

from classes_principales import (
    Membre,
    TacheExt,
    Risque,
    Jalon,
    Changement,
    ProjetNotifiable,
    EmailNotificationStrategy,
    calculer_chemin_critique,
)


class TestProjet(unittest.TestCase):

    def setUp(self):
        self.projet = ProjetNotifiable(
            nom="Projet TER",
            description="Développement d'un systéme de gestion des passagers du TER",
            date_debut=datetime(2024, 1, 5),
            date_fin=datetime(2024, 6, 5),
            budget=300000,
            notification_strategy=EmailNotificationStrategy(),
        )

        self.membre1 = Membre("Ibrahima", "Développeur")
        self.membre2 = Membre("Thierno Adama", "Chef de projet")
        self.projet.ajouter_membre_equipe(self.membre1)
        self.projet.ajouter_membre_equipe(self.membre2)

        self.tache1 = TacheExt(
            nom="Développer l'API",
            description="Etape de création de l'API pour le projet",
            date_debut=datetime(2024, 1, 20),
            date_fin=datetime(2024, 2, 10),
            responsable=self.membre1,
            statut="Terminée",
        )

        self.tache2 = TacheExt(
            nom="Intégration des fonctionnalités",
            description="Etape d'intégration des fonctionnalités du systéme",
            date_debut=datetime(2024, 2, 15),
            date_fin=datetime(2024, 2, 28),
            responsable=self.membre2,
            statut="En cours",
        )
        self.tache2.ajouter_dependance(self.tache1)
        self.projet.ajouter_tache(self.tache1)
        self.projet.ajouter_tache(self.tache2)

        self.risque1 = Risque(
            description="Retard possible dû à des dépendances externes",
            probabilite=0.3,
            impact="Moyen",
        )
        self.projet.ajouter_risque(self.risque1)

        self.jalon1 = Jalon(nom="Phase 1 achevée", date=datetime(2024, 3, 5))
        self.projet.ajouter_jalon(self.jalon1)

        self.changement1 = Changement(
            description="Changement de la version de l'API",
            version="v1.1",
            date=datetime(2024, 3, 10),
        )
        self.projet.enregistrer_changement(self.changement1)

    def test_ajouter_membre(self):
        self.assertEqual(len(self.projet.equipe.membres), 2)
        self.assertEqual(self.projet.equipe.membres[0].nom, "Ibrahima")
        self.assertEqual(self.projet.equipe.membres[1].nom, "Thierno Adama")

    def test_ajouter_tache(self):
        self.assertEqual(len(self.projet.taches), 2)
        self.assertEqual(self.projet.taches[0].nom, "Développer l'API")
        self.assertEqual(self.projet.taches[1].nom, "Intégration des fonctionnalités")

    def test_ajouter_risque(self):
        self.assertEqual(len(self.projet.risques), 1)
        self.assertEqual(
            self.projet.risques[0].description,
            "Retard possible dû à des dépendances externes",
        )

    def test_ajouter_jalon(self):
        self.assertEqual(len(self.projet.jalons), 1)
        self.assertEqual(self.projet.jalons[0].nom, "Phase 1 achevée")

    def test_enregistrer_changement(self):
        self.assertEqual(len(self.projet.changements), 1)
        self.assertEqual(
            self.projet.changements[0].description, "Changement de la version de l'API"
        )

    def test_chemin_critique(self):
        chemin_critique = calculer_chemin_critique(self.projet)
        self.assertEqual(len(chemin_critique), 2)  # Attendu deux tâches
        noms_taches_critique = [tache.nom for tache in chemin_critique]
        self.assertIn("Développer l'API", noms_taches_critique)
        self.assertIn("Intégration des fonctionnalités", noms_taches_critique)

    def test_generer_rapport_activite(self):
        rapport = self.projet.generer_rapport_activite()
        self.assertIn("Rapport d'activité pour le projet: Projet TER", rapport)
        self.assertIn("Ibrahima (Développeur)", rapport)
        self.assertIn("Développer l'API", rapport)
        self.assertIn("Retard possible dû à des dépendances externes", rapport)
        self.assertIn("Phase 1 achevée", rapport)
        self.assertIn("Changement de la version de l'API", rapport)


if __name__ == "__main__":
    unittest.main()
