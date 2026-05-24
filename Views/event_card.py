import flet as ft
from Models.data import EventDTO


class EventCard(ft.Container):
    def __init__(self, event_data: EventDTO):
        super().__init__()

        self.event_data = event_data

        self.nom_text = ft.Text(
            self.event_data.nom,
            size=16,
            weight=ft.FontWeight.BOLD
        )

        self.content = ft.Column(
            controls=[
                self.nom_text,
                ft.Text(f"Date : {self.event_data.date}"),
                ft.Text(f"Heure : {self.event_data.heure}"),
                ft.Text(f"Salle : {self.event_data.salle}"),
                ft.Text(f"UE : {self.event_data.ue}"),
                ft.Text(f"Type : {self.event_data.type_cours}"),
                ft.ElevatedButton(
                    text="Éditer (Test)",
                    on_click=self.modifier_nom
                )
            ]
        )

        self.padding = 15
        self.border_radius = 10
        self.bgcolor = ft.colors.WHITE
        self.shadow = ft.BoxShadow(
            blur_radius=8,
            color=ft.colors.BLACK12
        )

    def modifier_nom(self, e):
        self.event_data.nom = "Nom Modifié"
        self.nom_text.value = self.event_data.nom
        self.update()