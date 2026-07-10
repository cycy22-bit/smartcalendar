import sqlite3
from typing import Optional

from Models import EnseignantDTO, EtudiantDTO, EventDTO, UserDTO


class DAO:
    """
    Classe de base des DAO SQLite.

    Tous les DAO peuvent utiliser le même fichier de base de données afin
    d'éviter qu'une nouvelle base en mémoire soit créée pour chaque objet DAO.
    """

    def __init__(self, db_path: str = "smartcalendar.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute("PRAGMA foreign_keys = ON")
        self._setup_db()

    def _setup_db(self) -> None:
        cursor = self.conn.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                google_linked INTEGER NOT NULL DEFAULT 0
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS enseignants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS uniteEnseignement (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code_ue TEXT NOT NULL UNIQUE,
                intitule TEXT NOT NULL,
                credits_ects INTEGER NOT NULL DEFAULT 0
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS promotion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nom_promo TEXT NOT NULL,
                annee_academique TEXT NOT NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS etudiant (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                matricule TEXT NOT NULL UNIQUE,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                promotion_id INTEGER,
                FOREIGN KEY (promotion_id)
                    REFERENCES promotion(id)
                    ON DELETE SET NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS cours (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                intitule_cours TEXT NOT NULL,
                volume_horaire INTEGER NOT NULL DEFAULT 0,
                id_enseignant INTEGER,
                id_ue INTEGER,
                FOREIGN KEY (id_enseignant)
                    REFERENCES enseignants(id)
                    ON DELETE SET NULL,
                FOREIGN KEY (id_ue)
                    REFERENCES uniteEnseignement(id)
                    ON DELETE SET NULL
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                types TEXT NOT NULL,
                date TEXT NOT NULL,
                heure_debut TEXT NOT NULL,
                heure_fin TEXT NOT NULL,
                est_synchro INTEGER NOT NULL DEFAULT 0,
                salle TEXT NOT NULL,
                cours_id INTEGER,
                FOREIGN KEY (cours_id)
                    REFERENCES cours(id)
                    ON DELETE SET NULL
            )
            """
        )

        self.conn.commit()

    def close(self) -> None:
        """Ferme proprement la connexion SQLite."""
        self.conn.close()


class BaseDAO:
    """
    DAO générique en mémoire.

    Cette classe est conservée si certaines parties du projet utilisent encore
    une liste Python au lieu de SQLite.
    """

    def __init__(self):
        self.data = []

    def get_by_id(self, object_id: int):
        """Recherche un objet à partir de l'un de ses identifiants connus."""
        id_attributes = (
            "id",
            "id_etudiant",
            "id_enseignant",
            "id_promotion",
            "id_ue",
            "id_cours",
            "id_seance",
        )

        for objet in self.data:
            for attribute in id_attributes:
                if hasattr(objet, attribute) and getattr(objet, attribute) == object_id:
                    return objet

        return None

    def get_all(self) -> list:
        """Retourne une copie de tous les objets enregistrés."""
        return list(self.data)

    def save(self, objet):
        """Ajoute un objet dans la liste et le retourne."""
        self.data.append(objet)
        return objet

    def delete(self, object_id: int) -> bool:
        """Supprime un objet à partir de son identifiant."""
        objet = self.get_by_id(object_id)

        if objet is None:
            return False

        self.data.remove(objet)
        return True


class UserDAO(DAO):
    def __init__(self, db_path: str = "smartcalendar.db"):
        super().__init__(db_path)

    def get_by_id(self, user_id: int) -> Optional[UserDTO]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, role, email, google_linked
            FROM users
            WHERE id = ?
            """,
            (user_id,),
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return UserDTO(*row)

    def get_all(self) -> list[UserDTO]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, role, email, google_linked
            FROM users
            ORDER BY id
            """
        )
        rows = cursor.fetchall()

        return [UserDTO(*row) for row in rows]

    def save(self, user: UserDTO) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO users (role, email, google_linked)
            VALUES (?, ?, ?)
            """,
            (
                user.role,
                user.email,
                int(bool(user.google_linked)),
            ),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def update(self, user: UserDTO) -> bool:
        user_id = getattr(user, "id", None)

        if user_id is None:
            user_id = getattr(user, "id_user", None)

        if user_id is None:
            raise ValueError("L'utilisateur ne possède aucun identifiant.")

        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE users
            SET role = ?, email = ?, google_linked = ?
            WHERE id = ?
            """,
            (
                user.role,
                user.email,
                int(bool(user.google_linked)),
                user_id,
            ),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def delete(self, user_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_by_email(self, email: str) -> Optional[UserDTO]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, role, email, google_linked
            FROM users
            WHERE email = ?
            """,
            (email,),
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return UserDTO(*row)


class EtudiantDAO(DAO):
    def __init__(self, db_path: str = "smartcalendar.db"):
        super().__init__(db_path)

    def get_by_id(self, etudiant_id: int) -> Optional[EtudiantDTO]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, matricule, nom, prenom, email
            FROM etudiant
            WHERE id = ?
            """,
            (etudiant_id,),
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return EtudiantDTO(*row)

    def get_all(self) -> list[EtudiantDTO]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, matricule, nom, prenom, email
            FROM etudiant
            ORDER BY id
            """
        )
        rows = cursor.fetchall()

        return [EtudiantDTO(*row) for row in rows]

    def save(self, etudiant: EtudiantDTO, promotion_id: int | None = None) -> int:
        if promotion_id is None:
            promotion_id = getattr(etudiant, "promotion_id", None)

        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO etudiant (
                matricule,
                nom,
                prenom,
                email,
                promotion_id
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                etudiant.matricule,
                etudiant.nom,
                etudiant.prenom,
                etudiant.email,
                promotion_id,
            ),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def update(self, etudiant: EtudiantDTO) -> bool:
        etudiant_id = getattr(etudiant, "id", None)

        if etudiant_id is None:
            etudiant_id = getattr(etudiant, "id_etudiant", None)

        if etudiant_id is None:
            raise ValueError("L'étudiant ne possède aucun identifiant.")

        promotion_id = getattr(etudiant, "promotion_id", None)

        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE etudiant
            SET matricule = ?,
                nom = ?,
                prenom = ?,
                email = ?,
                promotion_id = ?
            WHERE id = ?
            """,
            (
                etudiant.matricule,
                etudiant.nom,
                etudiant.prenom,
                etudiant.email,
                promotion_id,
                etudiant_id,
            ),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def delete(self, etudiant_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM etudiant WHERE id = ?", (etudiant_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def get_by_promotion(self, promotion_id: int) -> list[EtudiantDTO]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, matricule, nom, prenom, email
            FROM etudiant
            WHERE promotion_id = ?
            ORDER BY nom, prenom
            """,
            (promotion_id,),
        )
        rows = cursor.fetchall()

        return [EtudiantDTO(*row) for row in rows]


class EnseignantDAO(DAO):
    def __init__(self, db_path: str = "smartcalendar.db"):
        super().__init__(db_path)

    def get_by_id(self, enseignant_id: int) -> Optional[EnseignantDTO]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, nom, prenom
            FROM enseignants
            WHERE id = ?
            """,
            (enseignant_id,),
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return EnseignantDTO(*row)

    def get_all(self) -> list[EnseignantDTO]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT id, nom, prenom
            FROM enseignants
            ORDER BY nom, prenom
            """
        )
        rows = cursor.fetchall()

        return [EnseignantDTO(*row) for row in rows]

    def save(self, enseignant: EnseignantDTO) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            INSERT INTO enseignants (nom, prenom)
            VALUES (?, ?)
            """,
            (enseignant.nom, enseignant.prenom),
        )
        self.conn.commit()
        return int(cursor.lastrowid)

    def update(self, enseignant: EnseignantDTO) -> bool:
        enseignant_id = getattr(enseignant, "id", None)

        if enseignant_id is None:
            enseignant_id = getattr(enseignant, "id_enseignant", None)

        if enseignant_id is None:
            raise ValueError("L'enseignant ne possède aucun identifiant.")

        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE enseignants
            SET nom = ?, prenom = ?
            WHERE id = ?
            """,
            (
                enseignant.nom,
                enseignant.prenom,
                enseignant_id,
            ),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def delete(self, enseignant_id: int) -> bool:
        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM enseignants WHERE id = ?",
            (enseignant_id,),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def get_by_ue(self, ue_id: int) -> list[EnseignantDTO]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT DISTINCT
                enseignants.id,
                enseignants.nom,
                enseignants.prenom
            FROM enseignants
            INNER JOIN cours
                ON enseignants.id = cours.id_enseignant
            WHERE cours.id_ue = ?
            ORDER BY enseignants.nom, enseignants.prenom
            """,
            (ue_id,),
        )
        rows = cursor.fetchall()

        return [EnseignantDTO(*row) for row in rows]


class PromotionDAO(DAO):
    def __init__(self, db_path: str = "smartcalendar.db"):
        super().__init__(db_path)


class EventDAO(DAO):
    def __init__(self, db_path: str = "smartcalendar.db"):
        super().__init__(db_path)

    @staticmethod
    def _row_to_dto(row) -> EventDTO:
        """
        Transforme une ligne SQLite en EventDTO.

        Ordre attendu :
        id_seance, types, date, heure_debut, heure_fin,
        est_synchro, salle, cours_id.
        """
        return EventDTO(
            row[0],
            row[1],
            row[2],
            row[3],
            row[4],
            bool(row[5]),
            row[6],
            row[7],
        )

    def get_by_id(self, event_id: int) -> Optional[EventDTO]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT
                id,
                types,
                date,
                heure_debut,
                heure_fin,
                est_synchro,
                salle,
                cours_id
            FROM events
            WHERE id = ?
            """,
            (event_id,),
        )
        row = cursor.fetchone()

        if row is None:
            return None

        return self._row_to_dto(row)

    def get_all(self) -> list[EventDTO]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT
                id,
                types,
                date,
                heure_debut,
                heure_fin,
                est_synchro,
                salle,
                cours_id
            FROM events
            ORDER BY date, heure_debut
            """
        )
        rows = cursor.fetchall()

        return [self._row_to_dto(row) for row in rows]

    def save(self, event: EventDTO) -> int:
        cursor = self.conn.cursor()

        event_id = getattr(event, "id_seance", None)

        if event_id is None:
            cursor.execute(
                """
                INSERT INTO events (
                    types,
                    date,
                    heure_debut,
                    heure_fin,
                    est_synchro,
                    salle,
                    cours_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event.types,
                    event.date,
                    event.heure_debut,
                    event.heure_fin,
                    int(bool(event.est_synchro)),
                    event.salle,
                    event.cours_id,
                ),
            )
        else:
            cursor.execute(
                """
                INSERT INTO events (
                    id,
                    types,
                    date,
                    heure_debut,
                    heure_fin,
                    est_synchro,
                    salle,
                    cours_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    event_id,
                    event.types,
                    event.date,
                    event.heure_debut,
                    event.heure_fin,
                    int(bool(event.est_synchro)),
                    event.salle,
                    event.cours_id,
                ),
            )

        self.conn.commit()
        return int(cursor.lastrowid)

    def update(self, event: EventDTO) -> bool:
        event_id = getattr(event, "id_seance", None)

        if event_id is None:
            raise ValueError("L'événement ne possède aucun id_seance.")

        cursor = self.conn.cursor()
        cursor.execute(
            """
            UPDATE events
            SET types = ?,
                date = ?,
                heure_debut = ?,
                heure_fin = ?,
                est_synchro = ?,
                salle = ?,
                cours_id = ?
            WHERE id = ?
            """,
            (
                event.types,
                event.date,
                event.heure_debut,
                event.heure_fin,
                int(bool(event.est_synchro)),
                event.salle,
                event.cours_id,
                event_id,
            ),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def delete(self, event_or_id: EventDTO | int) -> bool:
        if isinstance(event_or_id, int):
            event_id = event_or_id
        else:
            event_id = getattr(event_or_id, "id_seance", None)

        if event_id is None:
            raise ValueError("Impossible de supprimer un événement sans identifiant.")

        cursor = self.conn.cursor()
        cursor.execute(
            "DELETE FROM events WHERE id = ?",
            (event_id,),
        )
        self.conn.commit()
        return cursor.rowcount > 0

    def get_by_event_type(self, event_type: str) -> list[EventDTO]:
        cursor = self.conn.cursor()
        cursor.execute(
            """
            SELECT
                id,
                types,
                date,
                heure_debut,
                heure_fin,
                est_synchro,
                salle,
                cours_id
            FROM events
            WHERE types = ?
            ORDER BY date, heure_debut
            """,
            (event_type,),
        )
        rows = cursor.fetchall()

        return [self._row_to_dto(row) for row in rows]