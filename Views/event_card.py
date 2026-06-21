import flet as ft

from Models import EventDTO

# TODO : Add EventDTO Name


class EventCard(ft.Container):
    def __init__(self, event: EventDTO):
        super().__init__()

        self.event_data = event

        self.nom_text = ft.Text(
            f"{self.event_data.cours_id}", size=16, weight=ft.FontWeight.BOLD
        )

        self.buton = ft.Button(
            content=ft.Text("Éditer (Test)"), on_click=self.modifier_nom
        )

        self.content = ft.Column(
            controls=[
                self.nom_text,
                ft.Text(f"Date : {self.event_data.date}"),
                ft.Text(f"Heure : {self.event_data.heure_debut}"),
                ft.Text(f"Salle : {self.event_data.salle}"),
                ft.Text(f"UE : {self.event_data.cours_id}"),  # TODO : Add EventDTO Name
                ft.Text(f"Type : {self.event_data.types}"),
                self.buton,
            ]
        )

        self.padding = 15
        self.border_radius = 10
        self.bgcolor = ft.Colors.WHITE
        self.shadow = ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK12)

    def modifier_nom(self, e):
        self.event_data.cours_id = 0  # TODO : Add EventDTO Name
        self.nom_text.value = f"{self.event_data.cours_id}"
        self.update()
