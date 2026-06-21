from datetime import date, time

from Models import EventDTO
from Models.data import TypeSeance
from Repositories import EventDAO


class AgendaService:
    def __init__(self):
        self.dao = EventDAO()

    # 🔹 Récupérer tous les événements
    def get_all_events(self) -> list[EventDTO]:
        return self.dao.get_all()

    # 🔹 Ajouter un événement
    def add_event(self, event: EventDTO) -> None:
        self.dao.save(event)

    # 🔹 Supprimer un événement
    def delete_event(self, event: EventDTO) -> None:
        self.dao.delete(event)

    # 🔹 Filtrer par type (TP, TD, CM)
    def get_events_by_type(self, type_event: str) -> list[EventDTO]:
        events = self.dao.get_by_event_type(type_event)
        return events

    # 🔹 Filtrer par date
    def get_events_by_date(self, date: str) -> list[EventDTO]:
        events = self.dao.get_all()
        return list(filter(lambda e: e.date == date, events))

    # 🔹 Filtrer combiné (type + date)
    def filter_events(self, type_event=None, date=None) -> list[EventDTO]:
        events = self.get_all_events()

        if type_event:
            # filter from events by type event using filter function and lambda
            events = list(filter(lambda e: e.types == type_event, events))

        if date:
            # filter events by date
            events = list(filter(lambda e: e.date == date, events))

        return events

    # 🔹 Générer des événements de test (remplace fake_events)
    def generate_fake_events(self) -> list[EventDTO]:
        return [
            EventDTO(
                id_seance=1,
                date_seance=date(month=5, day=24, year=2026),
                heure_debut=time(hour=8, minute=0),
                heure_fin=time(hour=10, minute=0),
                salle="Salle A",
                est_synchro=False,
                types=TypeSeance.COURS_MAGISTRAL,
                cours_id=1,
            ),
            EventDTO(
                id_seance=2,
                date_seance=date(month=5, day=24, year=2026),
                heure_debut=time(hour=10, minute=0),
                heure_fin=time(hour=12, minute=0),
                salle="Lab 1",
                est_synchro=False,
                types=TypeSeance.TP,
                cours_id=2,
            ),
            EventDTO(
                id_seance=3,
                date_seance=date(month=5, day=25, year=2026),
                heure_debut=time(hour=13, minute=0),
                heure_fin=time(hour=15, minute=0),
                salle="Salle B",
                est_synchro=False,
                types=TypeSeance.TD,
                cours_id=3,
            ),
        ]
