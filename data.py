from dataclasses import dataclass
from datetime import date, time
from enum import Enum, auto

from typing import List

class PromotionDTO:
    # Data Transfer Object for Promotion
    def __init__(self, id_promotion: int, nom_promo: str, annee_academique: str):
        self.id_promotion = id_promotion
        self.nom_promo = nom_promo
        self.annee_academique = annee_academique

        self.etudiants: List[EtudiantDTO] = []
        self.unites_enseignement: List[UniteEnseignementDTO] = []

@dataclass
class EtudiantDTO:
    def __init__(
        self,
        id_etudiant: int,
        matricule: str,
        nom: str,
        prenom: str,
        email: str,
        promotion_id: int,
    ):
        self.id_etudiant = id_etudiant
        self.matricule = matricule
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.promotion_id = promotion_id


class UniteEnseignementDTO:
    def __init__(
        self,
        id_ue: int,
        code_ue: str,
        intitule: str,
        credit_ects: int,
        promotion_id: int,
    ):
        self.id_ue = id_ue
        self.code_ue = code_ue
        self.intitule = intitule
        self.credit_ects = credit_ects
        self.promotion_id = promotion_id
        self.cours: List[CoursDTO] = []


class EnseignantDTO:
    def __init__(
        self,
        id_enseignant: int,
        nom: str,
        prenom: str,
        email: str,
    ):
        self.id_enseignant = id_enseignant
        self.nom = nom
        self.prenom = prenom
        self.email = email
        self.cours: List[CoursDTO] = []


class CoursDTO:
    def __init__(
        self,
        id_cours: int,
        intitule: str,
        volume_horaire: int,
        ue_id: int,
        enseignant_id: int,
    ):
        self.id_cours = id_cours
        self.intitule = intitule
        self.volume_horaire = volume_horaire
        self.ue_id = ue_id
        self.enseignant_id = enseignant_id

        self.seances: List[SeanceDTO] = []


class TypeSeance(Enum):
    COURS_MAGISTRAL = auto()
    TD = auto()
    TP = auto()
    EXAMEN = auto()
    AUTRE_EVENEMENT = auto()


class SeanceDTO:
    def __init__(
        self,
        id_seance: int,
        date_seance: date,
        heure_debut: time,
        heure_fin: time,
        salle: str,
        est_synchro: bool,
        cours_id: int,
        type: TypeSeance,
    ):
        self.id_seance = id_seance
        self.date = date_seance
        self.heure_debut = heure_debut
        self.heure_fin = heure_fin
        self.salle = salle
        self.est_synchro = est_synchro
        self.cours_id = cours_id
        self.type = type

class UserDTO:
    def __init__(
        self,
        id_user: int,
        email: str,
        password: str,
        role: str,
        google_link: str,

    ):
        self.id_user = id_user
        self.email = email
        self.password = password
        self.role = role
        self.google_link = google_link

class NotificationDTO:
    def __init__(
        self,
        id_notification: int,
        type: str,
        destinataire: list[str],
        message: str,
        date_envoi: date,
    
        
    ):
        self.id_notification = id_notification
        self.type = type
        self.destinataire = destinataire
        self.message = message
        self.date_envoi = date_envoi


