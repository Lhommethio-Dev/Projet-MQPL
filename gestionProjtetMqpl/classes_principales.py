from datetime import datetime
from typing import List


class Membre:
    """Classe représentant un membre de l'équipe."""

    def __init__(self, nom: str, role: str):
        self.nom = nom
        self.role = role


class Equipe:
    """Classe représentant une équipe."""

    def __init__(self):
        self.membres: List[Membre] = []

    def ajouter_membre(self, membre: Membre):
        """Ajoute un membre à l'équipe."""
        self.membres.append(membre)


class Jalon:
    """Classe représentant un jalon."""

    def __init__(self, nom: str, date: datetime):
        self.nom = nom
        self.date = date


class Risque:
    """Classe représentant un risque."""

    def __init__(self, description: str, probabilite: float, impact: str):
        self.description = description
        self.probabilite = probabilite
        self.impact = impact


class Tache:
    """Classe représentant une tâche."""

    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: datetime,
        date_fin: datetime,
        responsable: Membre,
        statut: str,
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.responsable = responsable
        self.statut = statut
        self.dependances: List[Tache] = []

        # Ajouter les propriétés pour la gestion du chemin critique
        self.duree = (self.date_fin - self.date_debut).days
        self.early_start = 0
        self.early_finish = 0
        self.late_start = 0
        self.late_finish = 0
        self.slack = 0

    def ajouter_dependance(self, tache: "Tache"):
        """Ajoute une dépendance à la tâche."""
        self.dependances.append(tache)


class Changement:
    """Classe représentant un changement."""

    def __init__(self, description: str, version: str, date: datetime):
        self.description = description
        self.version = version
        self.date = date


class Projet:
    """Classe représentant un projet."""

    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: datetime,
        date_fin: datetime,
        budget: float,
    ):
        self.nom = nom
        self.description = description
        self.date_debut = date_debut
        self.date_fin = date_fin
        self.budget = budget
        self.taches: List[Tache] = []
        self.equipe = Equipe()
        self.risques: List[Risque] = []
        self.jalons: List[Jalon] = []
        self.changements: List[Changement] = []

    def ajouter_tache(self, tache: Tache):
        """Ajoute une tâche au projet."""
        self.taches.append(tache)

    def ajouter_membre_equipe(self, membre: Membre):
        """Ajoute un membre à l'équipe du projet."""
        self.equipe.ajouter_membre(membre)

    def ajouter_risque(self, risque: Risque):
        """Ajoute un risque au projet."""
        self.risques.append(risque)

    def ajouter_jalon(self, jalon: Jalon):
        """Ajoute un jalon au projet."""
        self.jalons.append(jalon)

    def enregistrer_changement(self, changement: Changement):
        """Enregistre un changement pour le projet."""
        self.changements.append(changement)


class NotificationStrategy:
    """Interface pour la gestion des notifications."""

    def envoyer(self, message: str, membre: Membre):
        pass


class EmailNotificationStrategy(NotificationStrategy):
    """Gestion des notifications par email."""

    def envoyer(self, message: str, membre: Membre):
        print(f"Notification envoyée à {membre.nom} par email : {message}")


class SMSNotificationStrategy(NotificationStrategy):
    """Gestion des notifications par SMS."""

    def envoyer(self, message: str, membre: Membre):
        print(f"Envoi d'un SMS à {membre.nom} : {message}")


class NotificationContext:
    """Classe gérant les notifications en utilisant une stratégie."""

    def __init__(self, strategy: NotificationStrategy):
        self.strategy = strategy

    def notifier(self, message: str, membre: Membre):
        """Envoie une notification au membre."""
        self.strategy.envoyer(message, membre)


class ProjetNotifiable(Projet):
    """Classe étendue pour ajouter des notifications au projet."""

    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: datetime,
        date_fin: datetime,
        budget: float,
        notification_strategy: NotificationStrategy,
    ):
        super().__init__(nom, description, date_debut, date_fin, budget)
        self.notification_context = NotificationContext(notification_strategy)

    def ajouter_tache(self, tache: Tache):
        """Ajoute une tâche et notifie tous les membres."""
        super().ajouter_tache(tache)
        self.notifier_tous_membres(f"Nouvelle tâche ajoutée: {tache.nom}")

    def ajouter_membre_equipe(self, membre: Membre):
        """Ajoute un membre à l'équipe et notifie tous les membres."""
        super().ajouter_membre_equipe(membre)
        self.notifier_tous_membres(f"Nouvel membre ajouté: {membre.nom}")

    def ajouter_risque(self, risque: Risque):
        """Ajoute un risque et notifie tous les membres."""
        super().ajouter_risque(risque)
        self.notifier_tous_membres(f"Nouveau risque ajouté: " f"{risque.description}")

    def ajouter_jalon(self, jalon: Jalon):
        """Ajoute un jalon et notifie tous les membres."""
        super().ajouter_jalon(jalon)
        self.notifier_tous_membres(f"Nouveau jalon ajouté: {jalon.nom}")

    def enregistrer_changement(self, changement: Changement):
        """Enregistre un changement et notifie tous les membres."""
        super().enregistrer_changement(changement)
        self.notifier_tous_membres(
            f"Nouveau changement enregistré: "
            f"{changement.description} version: {changement.version}"
        )

    def notifier_tous_membres(self, message: str):
        """Notifie tous les membres de l'équipe."""
        for membre in self.equipe.membres:
            self.notification_context.notifier(message, membre)

    def generer_rapport_activite(self):
        """Génère et retourne un rapport d'activité pour le projet."""
        rapport = f"Rapport d'activité pour le projet: {self.nom}\n"
        rapport += f"Description: {self.description}\n"
        rapport += (
            f"Dates: {self.date_debut.strftime('%Y-%m-%d')}"
            f" - {self.date_fin.strftime('%Y-%m-%d')}\n"
        )
        rapport += f"Budget: {self.budget}\n\n"

        rapport += "Membres de l'équipe:\n"
        for membre in self.equipe.membres:
            rapport += f" - {membre.nom} ({membre.role})\n"

        rapport += "\nTâches:\n"
        for tache in self.taches:
            rapport += (
                f" - {tache.nom}: {tache.description}, "
                f"Responsable: {tache.responsable.nom}, "
                f"Statut: {tache.statut}, "
                f"Début: {tache.date_debut.strftime('%Y-%m-%d')}, "
                f"Fin: {tache.date_fin.strftime('%Y-%m-%d')}\n"
            )

        rapport += "\nRisques:\n"
        for risque in self.risques:
            rapport += (
                f" - {risque.description}, "
                f"Probabilité: {risque.probabilite}, Impact: {risque.impact}\n"
            )

        rapport += "\nJalons:\n"
        for jalon in self.jalons:
            rapport += f" - {jalon.nom}: {jalon.date.strftime('%Y-%m-%d')}\n"
        rapport += "\nChangements:\n"
        for changement in self.changements:
            rapport += (
                f" - {changement.description}, "
                f"Version: {changement.version}, "
                f"Date: {changement.date.strftime('%Y-%m-%d')}\n"
            )

        return rapport


class TacheExt(Tache):
    """Classe étendue de tâche pour CPM et rapport d'activité."""

    def __init__(
        self,
        nom: str,
        description: str,
        date_debut: datetime,
        date_fin: datetime,
        responsable: Membre,
        statut: str,
    ):
        super().__init__(nom, description, date_debut, date_fin, responsable, statut)
        self.duree = (self.date_fin - self.date_debut).days
        self.early_start = 0
        self.early_finish = 0
        self.late_start = 0
        self.late_finish = 0
        self.slack = 0


def calculer_chemin_critique(projet: ProjetNotifiable):
    """Calcule le chemin critique pour le projet."""
    taches = [t for t in projet.taches if isinstance(t, TacheExt)]
    for tache in taches:
        tache.early_start = 0
        tache.early_finish = tache.duree

    for tache in taches:
        for dependance in tache.dependances:
            dependance.early_start = max(dependance.early_start, tache.early_finish)
            dependance.early_finish = dependance.early_start + dependance.duree

    total_duree = max(tache.early_finish for tache in taches)

    for tache in taches:
        tache.late_finish = total_duree
        tache.late_start = tache.late_finish - tache.duree

    for tache in reversed(taches):
        for dependance in tache.dependances:
            tache.late_finish = min(tache.late_finish, dependance.late_start)
            tache.late_start = tache.late_finish - tache.duree

    for tache in taches:
        tache.slack = tache.late_start - tache.early_start

    chemin_critique = [tache for tache in taches if tache.slack == 0]
    return chemin_critique


# Cas d'utilisation
if __name__ == "__main__":
    # Création du projet
    projet = ProjetNotifiable(
        nom="Projet TER",
        description="Développement d'un " "systéme de gestion des passagers du TER",
        date_debut=datetime(2024, 1, 5),
        date_fin=datetime(2024, 6, 5),
        budget=300000,
        notification_strategy=EmailNotificationStrategy(),
    )

    # Ajout des membres à l'équipe
    membre1 = Membre("Ibrahima", "Développeur")
    membre2 = Membre("Thierno Adama", "Chef de projet")
    membre3 = Membre("Seydina Ababacar", "Coordinateur")
    projet.ajouter_membre_equipe(membre1)
    projet.ajouter_membre_equipe(membre2)
    projet.ajouter_membre_equipe(membre3)

    # Ajout des tâches
    tache1 = TacheExt(
        nom="Développer l'API",
        description="Etape de création de l'API pour le projet",
        date_debut=datetime(2024, 1, 20),
        date_fin=datetime(2024, 2, 10),
        responsable=membre1,
        statut="Terminée",
    )
    tache2 = TacheExt(
        nom="Intégration des fonctionnalités",
        description="Etape d'intégration des fonctionnalités du systéme",
        date_debut=datetime(2024, 2, 15),
        date_fin=datetime(2024, 2, 28),
        responsable=membre2,
        statut="En cours",
    )
    tache2.ajouter_dependance(tache1)
    projet.ajouter_tache(tache1)
    projet.ajouter_tache(tache2)

    # Ajout d'un risque
    risque1 = Risque(
        description="Retard possible dû à des dépendances externes",
        probabilite=0.3,
        impact="Moyen",
    )
    projet.ajouter_risque(risque1)

    # Ajout d'un jalon
    jalon1 = Jalon(nom="Phase 1 achevée", date=datetime(2024, 3, 5))
    projet.ajouter_jalon(jalon1)

    # Enregistrement d'un changement
    changement1 = Changement(
        description="Changement de la version de l'API",
        version="v1.1",
        date=datetime(2024, 3, 10),
    )
    projet.enregistrer_changement(changement1)

    print("#################################################################")
    print("#################################################################")

    # Calculer le chemin critique
    chemin_critique = calculer_chemin_critique(projet)
    print("Chemin Critique:")
    for tache in chemin_critique:
        print(
            f"Tâche: {tache.nom}, Début: "
            f"{tache.date_debut}, Fin: "
            f"{tache.date_fin}, Durée: {tache.duree} jours"
        )

    # Générer et afficher le rapport d'activité
    rapport = projet.generer_rapport_activite()
    print("\n" + rapport)
