# Exercice 1
## Implémentation des DAOs des modèles DTO suivant le diagramme class_comp.puml

# Avec Python, les class Interfaces peuvent être implémentées comme des classes abstraites
# heritant de Protocol
import sqlite3
from random import randint
from typing import List, Optional, Protocol

from Models import EnseignantDTO, EtudiantDTO, EventDTO, UserDTO


# Exercice 2
class DAO:
    def __init__(self, db_path: str = ":memory:"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self._setup_db()

    def _setup_db(self):
        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                email TEXT,
                google_linked BOOLEAN
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enseignants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT,
                prenom TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS uniteEnseignement (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_ue TEXT,
                intitule TEXT,
                credits_ects INTEGER
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS promotion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_promo TEXT,
                annee_academique TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS etudiant (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricule TEXT,
                nom TEXT,
                prenom TEXT,
                email TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS cours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intitule_cours TEXT,
                volume_horaire INTEGER,
                id_enseignant INTEGER,
                id_ue INTEGER,
                FOREIGN KEY (id_enseignant) REFERENCES enseignants(id),
                FOREIGN KEY (id_ue) REFERENCES uniteEnseignement(id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date_seance DATETIME,
                heure_debut TIME,
                heure_fin TIME,
                salle TEXT,
                est_synchro BOOLEAN,
                types TEXT,
                id_cours INTEGER,
                FOREIGN KEY (id_cours) REFERENCES cours(id)
            )
        """)
        self.conn.commit()


class BaseDAO(Protocol):
    def get_by_id(self, id) -> DAO: ...

    def get_all(self) -> list[DAO]: ...

    def save(self, obj) -> int | None: ...

    def update(self, obj) -> int | None: ...

    def delete(self, obj) -> int | None: ...


class UserDAO(DAO):
    def __init__(
        self,
    ):
        # Initialisation de la connexion à la base de données
        super().__init__()

    def get_by_id(self, id: int) -> Optional[UserDTO]:
        cursor = self.conn.cursor()
        # Requete de récupération d'un utilisateur par son ID
        cursor.execute("SELECT id, role, email, logedin FROM users WHERE id = ?", (id,))
        id_user, role, email, logedin = cursor.fetchone()

        if not id_user:
            return None

        return UserDTO(id_user, role, email, logedin)

    def get_all(self) -> List[UserDTO]:
        cursor = self.conn.cursor()
        # Requete de récupération de tous les utilisateurs
        cursor.execute("SELECT * FROM users")

        return [UserDTO(r[0], r[1], r[2], r[3]) for r in cursor.fetchall()]

    def save(self, user: UserDTO) -> int | None:
        cursor = self.conn.cursor()
        auto_id = (
            user.id_user
            if user.id_user
            else (
                randint(1, 100) + cursor.lastrowid
                if cursor.lastrowid
                else randint(1, 100)
            )
        )
        cursor.execute(
            "INSERT INTO users (id, role, email, logedin) VALUES (?, ?, ?, ?)",
            (auto_id, user.role, user.email, user.logedin),
        )
        self.conn.commit()
        return cursor.lastrowid

    def update(self, user: UserDTO) -> int | None:
        cursor = self.conn.cursor()
        role, email, logedin, id = (
            user.role,
            user.email,
            user.logedin,
            user.id_user,
        )
        cursor.execute(
            "UPDATE users SET role = ? , email = ? , logedin = ? WHERE id = ?",
            (role, email, logedin, id),
        )
        self.conn.commit()
        return cursor.lastrowid

    def delete(self, user: UserDTO) -> int | None:
        cursor = self.conn.cursor()
        id = user.id_user
        cursor.execute(
            "DELETE FROM users WHERE id = ?",
            (id,),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_by_email(self, user: UserDTO) -> Optional[UserDTO]:
        cursor = self.conn.cursor()
        email = user.email
        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,),
        )
        result = cursor.fetchone()
        if result:
            return UserDTO(result[0], result[1], result[2], result[3])
        return None


class EtudiantDAO(DAO):
    def __init__(self):
        super().__init__()

    def get_by_id(self, id) -> Optional[EtudiantDTO]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM etudiant WHERE id = ?", (id,))
        row = cursor.fetchone()

        if row is None:
            return None

        return EtudiantDTO(*row)

    def get_all(self) -> list[EtudiantDTO]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM etudiant")
        rows = cursor.fetchall()

        return [EtudiantDTO(*row) for row in rows]

    def save(self, etudiant: EtudiantDTO) -> int | None:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO etudiant (matricule, nom, prenom, email)
            VALUES (?, ?, ?, ?)
            """,
            (etudiant.matricule, etudiant.nom, etudiant.prenom, etudiant.email),
        )

        self.conn.commit()

        return cursor.lastrowid

    def delete(self, id: int) -> int | None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM etudiant WHERE id = ?", (id,))
        self.conn.commit()

    def get_by_promotion(self, promotion_id) -> list[EtudiantDTO]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM etudiant WHERE promotion_id = ?", (promotion_id,))
        rows = cursor.fetchall()

        return [EtudiantDTO(*row) for row in rows]


class EnseignantDAO(DAO):
    def __init__(self):
        super().__init__()

    def get_by_id(self, id) -> Optional[EnseignantDTO]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM enseignants WHERE id = ?", (id,))
        row = cursor.fetchone()

        if row is None:
            return None

        return EnseignantDTO(*row)

    def get_all(self) -> list[EnseignantDTO]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM enseignants")
        rows = cursor.fetchall()

        return [EnseignantDTO(*row) for row in rows]

    def save(self, enseignant: EnseignantDTO) -> int | None:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            INSERT INTO enseignants (nom, prenom)
            VALUES (?, ?)
            """,
            (enseignant.nom, enseignant.prenom),
        )

        self.conn.commit()

        return cursor.lastrowid

    def delete(self, id_enseignant) -> int | None:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM enseignants WHERE id = ?", (id_enseignant,))
        self.conn.commit()

    def get_by_ue(self, ue_id) -> list[EnseignantDTO]:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT enseignants.*
            FROM enseignants
            INNER JOIN cours ON enseignants.id = cours.id_enseignant
            WHERE cours.id_ue = ?
            """,
            (ue_id,),
        )

        rows = cursor.fetchall()

        return [EnseignantDTO(*row) for row in rows]


class PromotionDAO(DAO):
    def __init__(self) -> None:
        super().__init__()


class EventDAO(DAO):
    def __init__(self):
        super().__init__()

    def get_by_id(self, id: int) -> Optional[EventDTO]:
        cursor = self.conn.cursor()
        # Requete de récupération d'un événement par son ID
        cursor.execute(
            "SELECT id, types, date, heure_debut, heure_fin, est_synchro, salle, cours_id FROM events WHERE id = ?",
            (id,),
        )
        id_event, types, date, heure_debut, heure_fin, est_synchro, salle, cours_id = (
            cursor.fetchone()
        )

        if not id_event:
            return None

        return EventDTO(
            id_event, types, date, heure_debut, heure_fin, est_synchro, salle, cours_id
        )

    def get_all(self) -> List[EventDTO]:
        cursor = self.conn.cursor()
        # Requete de récupération de tous les événements
        cursor.execute("SELECT * FROM events")

        return [
            EventDTO(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7])
            for r in cursor.fetchall()
        ]

    def save(self, event: EventDTO) -> int | None:
        cursor = self.conn.cursor()
        auto_id = (
            event.id_seance
            if event.id_seance
            else (
                randint(1, 100) + cursor.lastrowid
                if cursor.lastrowid
                else randint(1, 100)
            )
        )
        cursor.execute(
            "INSERT INTO events (id, types, date, heure_debut, heure_fin, est_synchro, salle, cours_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                auto_id,
                event.types,
                event.date,
                event.heure_debut,
                event.heure_fin,
                event.est_synchro,
                event.salle,
                event.cours_id,
            ),
        )
        self.conn.commit()
        return cursor.lastrowid

    def update(self, event: EventDTO) -> int | None:
        cursor = self.conn.cursor()
        types, date, heure_debut, heure_fin, est_synchro, salle, cours_id, id = (
            event.types,
            event.date,
            event.heure_debut,
            event.heure_fin,
            event.est_synchro,
            event.salle,
            event.cours_id,
            event.id_seance,
        )
        cursor.execute(
            "UPDATE events SET types = ? , date = ? , heure_debut = ? , heure_fin = ? , est_synchro = ? , salle = ? , cours_id = ? WHERE id = ?",
            (types, date, heure_debut, heure_fin, est_synchro, salle, cours_id, id),
        )
        self.conn.commit()
        return cursor.lastrowid

    def delete(self, event: EventDTO) -> int | None:
        cursor = self.conn.cursor()
        id = event.id_seance
        cursor.execute(
            "DELETE FROM events WHERE id = ?",
            (id,),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_by_event_type(self, event_type: str) -> List[EventDTO]:
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT * FROM events WHERE types = ?",
            (event_type,),
        )
        result = cursor.fetchall()
        if result:
            return [
                EventDTO(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7]) for r in result
            ]
        return []
