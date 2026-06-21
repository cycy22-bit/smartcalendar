import time

import flet as ft

from Services.agenda_services import AgendaService
from Views.event_card import EventCard


class AuthView(ft.Container):
    def __init__(self):
        super().__init__()
        # self.agenda_service = AgendaService()
        # self.events = self.agenda_service.generate_fake_events()

        self.email = ft.TextField(label="Email")
        self.password = ft.TextField(label="Mot de passe", password=True)
        self.message = ft.Text("", color=ft.Colors.RED)

        # Le callback on_click appelle notre méthode de validation
        self.button = ft.FilledButton("Se connecter", on_click=self.valider_saisie)

        # On centre le contenu et on prend tout l'espace (Propriétés du Container)
        self.alignment = ft.Alignment.CENTER
        self.expand = True

    def build(self):
        """
        La méthode build() doit construire la structure imbriquée de votre composant
        et retourner obligatoirement le contrôle racine (ici la colonne).
        """
        self.content = ft.Column(
            width=350,
            controls=[
                ft.Text(
                    "Connexion SmartCalendrier", size=24, weight=ft.FontWeight.BOLD
                ),
                self.email,
                self.password,
                self.button,
                self.message,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )

    async def valider_saisie(self, e):
        """
        En enlevant le mot-clé async, la méthode devient synchrone et compatible
        directement avec le gestionnaire d'événements par défaut du bouton Flet.
        """
        if self.email.value == "" or self.password.value == "":
            self.message.value = "Veuillez remplir tous les champs."
            self.update()
        else:
            page = self.page

            if isinstance(page, ft.Page):
                await page.push_route("/dashboard")


class DashboardView(ft.Container):
    def __init__(self):
        super().__init__()

    def build(self):
        self.content = ft.Column(
            controls=[
                ft.Text(
                    "Dashboard SmartCalendrier", size=28, weight=ft.FontWeight.BOLD
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Text("Cours aujourd'hui : 3"),
                            padding=20,
                            bgcolor=ft.Colors.BLUE_50,
                        ),
                        ft.Container(
                            content=ft.Text("Notifications : 5"),
                            padding=20,
                            bgcolor=ft.Colors.BLUE_50,
                        ),
                        ft.Container(
                            content=ft.Text("Synchronisations : 2"),
                            padding=20,
                            bgcolor=ft.Colors.BLUE_50,
                        ),
                    ]
                ),
            ]
        )

        self.padding = 30
        self.expand = True


class CalendarView(ft.Container):
    def __init__(self):
        super().__init__()

        self.agenda_service = AgendaService()

        self.events = self.agenda_service.generate_fake_events()

        self.list_view = ft.ListView(
            expand=True,
            spacing=10,
            controls=[
                ft.Draggable(
                    group="calendrier",
                    content=EventCard(event),
                    content_feedback=ft.Container(
                        content=ft.Text(f"{event.cours_id}"),
                        bgcolor=ft.Colors.BLUE_100,
                        padding=10,
                    ),
                )
                for event in self.events
            ],
        )

        self.drop_message = ft.Text("Déposez une carte ici.")
        self.drop_zone = ft.DragTarget(
            group="calendrier",
            content=ft.Container(
                width=300,
                height=120,
                bgcolor=ft.Colors.GREY_200,
                border_radius=10,
                alignment=ft.Alignment.CENTER,
                content=self.drop_message,
            ),
            on_accept=self.on_accept,
        )

        self.content = ft.Column(
            controls=[
                ft.Text(
                    "Calendrier avec Drag & Drop", size=26, weight=ft.FontWeight.BOLD
                ),
                self.drop_zone,
                self.list_view,
            ]
        )

        self.padding = 30
        self.expand = True

    def on_accept(self, e):
        self.drop_zone.content.page.bgcolor = ft.Colors.GREEN_100
        self.drop_message.value = "Évènement déposé avec succès."

        self.page.show_dialog(
            dialog=ft.SnackBar(
                content=ft.Text("Carte déposée dans le calendrier"),
                open=True,
            )
        )


class ImportView(ft.Container):
    def __init__(self):
        super().__init__()

    def build(self):
        self.file_path = ft.Text("Aucun fichier sélectionné.")
        self.table = ft.DataTable(
            columns=[
                ft.DataColumn(label=ft.Text("Date")),
                ft.DataColumn(label=ft.Text("Heure")),
                ft.DataColumn(label=ft.Text("Nom")),
                ft.DataColumn(label=ft.Text("Salle")),
            ],
            rows=[],
        )

        self.file_picker = ft.FilePicker(on_upload=self.file_selected)

        self.pick_file_button = ft.Button(
            "Sélectionner fichier CSV/XLSX", on_click=self.pick_file
        )

    def did_mount(self):
        self.content = ft.Column(
            controls=[
                ft.Text("Importation CSV / XLSX", size=26, weight=ft.FontWeight.BOLD),
                self.pick_file_button,
                self.file_path,
                self.table,
            ]
        )

        self.padding = 30
        self.expand = True
        self.page.overlay.append(self.file_picker)
        self.page.update()

    async def pick_file(self, e):
        await self.file_picker.pick_files(
            allow_multiple=False, allowed_extensions=["csv", "xlsx"]
        )

    async def file_selected(self, e):
        if e.files:
            self.file_path.value = f"Fichier sélectionné : {e.files[0].path}"

            self.table.rows = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("2026-05-24")),
                        ft.DataCell(ft.Text("08h00")),
                        ft.DataCell(ft.Text("Mathématiques")),
                        ft.DataCell(ft.Text("Salle A")),
                    ]
                ),
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("2026-05-24")),
                        ft.DataCell(ft.Text("10h00")),
                        ft.DataCell(ft.Text("Électronique")),
                        ft.DataCell(ft.Text("Lab 1")),
                    ]
                ),
            ]

            self.update()


class FilterView(ft.Container):
    def __init__(self):
        super().__init__()

    def build(self):
        self.agenda_service = AgendaService()
        self.events = self.agenda_service.generate_fake_events()
        self.check_tp = ft.Checkbox(label="TP", value=True, on_change=self.apply_filter)
        self.check_td = ft.Checkbox(label="TD", value=True, on_change=self.apply_filter)
        self.check_cm = ft.Checkbox(label="CM", value=True, on_change=self.apply_filter)

        self.event_list = ft.ListView(expand=True, spacing=10)

    def did_mount(self):
        self.content = ft.Column(
            controls=[
                ft.Text("Filtres interactifs", size=26, weight=ft.FontWeight.BOLD),
                ft.Row([self.check_tp, self.check_td, self.check_cm]),
                self.event_list,
            ]
        )

        self.padding = 30
        self.expand = True
        self.apply_filter(None)

    def apply_filter(self, e):
        types_actifs = []

        if self.check_tp.value:
            types_actifs.append("TP")
        if self.check_td.value:
            types_actifs.append("TD")
        if self.check_cm.value:
            types_actifs.append("CM")

        self.event_list.controls = [
            EventCard(event) for event in self.events if event.types in types_actifs
        ]

        self.update()


class SyncView(ft.Container):
    def __init__(self):
        super().__init__()

        self.progress = ft.ProgressRing(visible=False)
        self.message = ft.Text("")
        self.button = ft.Button("Synchroniser avec Google", on_click=self.synchroniser)

        self.content = ft.Column(
            controls=[
                ft.Text("Synchronisation Google", size=26, weight=ft.FontWeight.BOLD),
                self.button,
                self.progress,
                self.message,
            ]
        )

        self.padding = 30
        self.expand = True

    def synchroniser(self, e):
        self.progress.visible = True
        self.message.value = "Synchronisation en cours..."
        self.update()

        time.sleep(2)

        self.progress.visible = False
        self.message.value = "Synchronisation réussie avec Google."
        self.message.color = ft.Colors.GREEN
        self.update()
