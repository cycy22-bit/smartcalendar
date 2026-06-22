from Models.data import EventDTO
from Repositories.dao import EventDAO


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
    def delete_event(self, event_id: int) -> None:
        self.dao.delete(event_id)

    # 🔹 Filtrer par type (TP, TD, CM)
    def get_events_by_type(self, type_cours: str) -> list[EventDTO]:
        events = self.dao.get_all()
        return [e for e in events if e.type_cours == type_cours]

    # 🔹 Filtrer par date
    def get_events_by_date(self, date: str) -> list[EventDTO]:
        events = self.dao.get_all()
        return [e for e in events if e.date == date]

    # 🔹 Filtrer combiné (type + date)
    def filter_events(self, type_cours=None, date=None) -> list[EventDTO]:
        events = self.dao.get_all()

        if type_cours:
            events = [e for e in events if e.type_cours == type_cours]

        if date:
            events = [e for e in events if e.date == date]

        return events

    # 🔹 Générer des événements de test (remplace fake_events)
    def generate_fake_events(self) -> list[EventDTO]:
        return [
            EventDTO(1, "Mathématiques", "2026-05-24", "08h00", "Salle A", "Math", "CM"),
            EventDTO(2, "Électronique", "2026-05-24", "10h00", "Lab 1", "Elec", "TP"),
            EventDTO(3, "Informatique", "2026-05-25", "13h00", "Salle B", "Info", "TD"),
        ]