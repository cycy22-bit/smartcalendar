import asyncio
import time
from typing import Any

import flet as ft
from typing import cast

from Services.agenda_services import AgendaService
from Views.event_card import EventCard

# Variables d'état pour conserver les saisies et les messages entre les re-rendus
state_email = ""
state_password = ""
state_message = ""


@ft.component
def AuthView():
    global state_email, state_password, state_message

    # Références locales pour lire les valeurs saisies au clic
    email_field = ft.TextField(label="Email", value=state_email)
    password_field = ft.TextField(
        label="Mot de passe", password=True, value=state_password
    )
    message_text = ft.Text(state_message, color=ft.Colors.RED)

    def valider_saisie(e):
        global state_email, state_password, state_message

        # Sauvegarde des saisies actuelles dans l'état
        state_email = email_field.value
        state_password = password_field.value

        if state_email == "" or state_password == "":
            state_message = "Veuillez remplir tous les champs."
            # On met à jour l'arbre déclaratif globalement via la page
            ft.context.page.update()
        else:
            state_message = ""
            # Navigation sécurisée vers le tableau de bord
            ft.context.page.navigate("/dashboard")
            ft.context.page.update()

    button = ft.FilledButton("Se connecter", on_click=valider_saisie)

    # Retour déclaratif de la structure complète
    return ft.Container(
        alignment=ft.Alignment.CENTER,
        expand=True,
        content=ft.Column(
            width=350,
            controls=[
                ft.Text(
                    "Connexion SmartCalendrier", size=24, weight=ft.FontWeight.BOLD
                ),
                email_field,
                password_field,
                button,
                message_text,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
    )


@ft.component
def DashboardView():
    # Retour déclaratif direct de l'arborescence complète
    return ft.Container(
        padding=30,
        expand=True,
        content=ft.Column(
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
        ),
    )


# Pour éviter de régénérer les événements à chaque re-rendu de la fonction
agenda_service = AgendaService()
fake_events = agenda_service.generate_fake_events()

# Variable d'état déclarative globale pour piloter l'interface
state_is_dropped = False


@ft.component
def CalendarView():
    global state_is_dropped

    def on_accept(e):
        global state_is_dropped
        # 1. Mise à jour de l'état
        state_is_dropped = True

        # 2. Ajout sécurisé du SnackBar dans l'overlay via le contexte déclaratif
        page = ft.context.page
        page.overlay.append(
            ft.SnackBar(
                content=ft.Text("Carte déposée dans le calendrier"),
                open=True,
            )
        )

        # 3. Demande au moteur de reconstruire l'arbre visuel
        page.update()

    # --- RECONSTRUCTION DE L'ARBRE (DÉCLARATIF) ---

    list_view = ft.ListView(
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
            for event in fake_events
        ],
    )

    # Choix du texte de la zone de dépôt selon l'état actuel
    texte_message = (
        "Évènement déposé avec succès."
        if state_is_dropped
        else "Déposez une carte ici."
    )

    drop_zone = ft.DragTarget(
        group="calendrier",
        content=ft.Container(
            width=300,
            height=120,
            bgcolor=ft.Colors.GREY_200,
            border_radius=10,
            alignment=ft.Alignment.CENTER,
            content=ft.Text(texte_message),
        ),
        on_accept=on_accept,
    )

    # Contenu global de la colonne
    contenu_colonne = ft.Column(
        controls=[
            ft.Text(
                "Calendrier avec Drag & Drop",
                size=26,
                weight=ft.FontWeight.BOLD,
            ),
            drop_zone,
            list_view,
        ]
    )

    # Structure conditionnelle du design selon l'état (Fond vert ou transparent)
    if state_is_dropped:
        affichage_interne = ft.Container(
            bgcolor=ft.Colors.GREEN_100,
            padding=15,
            border_radius=10,
            content=contenu_colonne,
        )
    else:
        affichage_interne = contenu_colonne

    # Renvoi du Container d'affichage principal
    return ft.Container(padding=30, expand=True, content=affichage_interne)


# Variables d'état partagées pour le rendu déclaratif
state_file_path = "Aucun fichier sélectionné."
state_table_rows = []

# Référence de l'instance persistante du FilePicker pour le routeur
file_picker_instance = None


@ft.component
def ImportView():
    global state_file_path, state_table_rows, file_picker_instance

    # 1. Le callback s'exécute lorsque l'utilisateur valide la boîte de dialogue
    def handle_picker_result(e: ft.FilePickerUploadEvent):
        global state_file_path, state_table_rows
        if e.file_name:
            # On extrait le nom du fichier sélectionné
            state_file_path = f"Fichier sélectionné : {e.file_name}"

            # Injection des nouvelles lignes dans l'état global
            state_table_rows = [
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
            # On force la reconstruction de la vue via la page globale
            ft.context.page.update()

    # 2. Initialisation unique du FilePicker pour éviter les duplications
    if file_picker_instance is None:
        file_picker_instance = ft.FilePicker(on_upload=handle_picker_result)

    # 3. Fonction asynchrone pour ouvrir l'explorateur natif au clic
    async def pick_file_click(e):
        if file_picker_instance:
            await file_picker_instance.pick_files(
                allow_multiple=False, allowed_extensions=["csv", "xlsx"]
            )

    # 4. Rattachement sécurisé du composant invisible à l'overlay de la page
    page = ft.context.page
    if page and file_picker_instance not in page.overlay:
        page.overlay.append(file_picker_instance)

    # --- RECONSTRUCTION DE L'ARBRE (DÉCLARATIF) ---

    return ft.Container(
        padding=30,
        expand=True,
        content=ft.Column(
            controls=[
                ft.Text("Importation CSV / XLSX", size=26, weight=ft.FontWeight.BOLD),
                ft.Button(
                    "Sélectionner fichier CSV/XLSX",
                    icon=ft.Icons.UPLOAD_FILE,
                    on_click=pick_file_click,
                ),
                ft.Text(state_file_path),
                ft.DataTable(
                    columns=[
                        ft.DataColumn(label=ft.Text("Date")),
                        ft.DataColumn(label=ft.Text("Heure")),
                        ft.DataColumn(label=ft.Text("Nom")),
                        ft.DataColumn(label=ft.Text("Salle")),
                    ],
                    rows=state_table_rows,  # Chargement dynamique depuis les variables d'état
                ),
            ]
        ),
    )


# Pour éviter de régénérer la liste à chaque re-rendu déclaratif
agenda_service = AgendaService()
all_events = agenda_service.generate_fake_events()

# États déclaratifs partagés pour suivre les filtres cochés
state_filters = {"TP": True, "TD": True, "CM": True}


@ft.component
def FilterView():
    global state_filters

    def on_checkbox_change(e: ft.ControlEvent):  # TODO
        global state_filters
        # Filtre les valeurs affichees en fonction de la valeur choisie par l'utilisateur au checkbox
        state_filters[e.control.key] = e.control.value
        ft.context.page.update()

    # --- FILTRAGE DÉCLARATIF DES ÉVÉNEMENTS ---
    types_actifs = [key for key, value in state_filters.items() if value]

    filtered_cards: list[ft.Control] = []
    for event in all_events:
        if hasattr(event, "types") and event.types in types_actifs:
            filtered_cards.append(EventCard(event))
        elif hasattr(event, "type") and event.types in types_actifs:
            filtered_cards.append(EventCard(event))

    # --- RECONSTRUCTION DE L'ARBRE VISUEL ---
    return ft.Container(
        padding=30,
        expand=True,
        content=ft.Column(
            controls=[
                ft.Text("Filtres interactifs", size=26, weight=ft.FontWeight.BOLD),
                ft.Row(
                    # cast() force le linter à accepter la liste comme une collection de Controls génériques
                    controls=cast(
                        list[ft.Control],
                        [
                            ft.Checkbox(
                                label="TP",
                                value=state_filters["TP"],
                                on_change=on_checkbox_change,
                            ),
                            ft.Checkbox(
                                label="TD",
                                value=state_filters["TD"],
                                on_change=on_checkbox_change,
                            ),
                            ft.Checkbox(
                                label="CM",
                                value=state_filters["CM"],
                                on_change=on_checkbox_change,
                            ),
                        ],
                    )
                ),
                ft.ListView(expand=True, spacing=10, controls=filtered_cards),
            ]
        ),
    )


# Variables d'état partagées pour le rendu déclaratif
state_progress_visible = False
state_message_value = ""
state_message_color = ft.Colors.RED  # Couleur de texte initiale par défaut


@ft.component
def SyncView():
    global state_progress_visible, state_message_value, state_message_color

    # La fonction devient asynchrone pour permettre un affichage fluide en temps réel
    async def synchroniser(e: ft.ControlEvent):
        global state_progress_visible, state_message_value, state_message_color

        # 1. ÉTAPE : Lancement de la synchronisation
        state_progress_visible = True
        state_message_value = "Synchronisation en cours..."
        ft.context.page.update()  # Premier rafraîchissement visuel pour afficher le ProgressRing

        # Utilisation de asyncio.sleep pour ne pas bloquer le thread de l'interface
        await asyncio.sleep(2)

        # 2. ÉTAPE : Fin de la synchronisation
        state_progress_visible = False
        state_message_value = "Synchronisation réussie avec Google."
        state_message_color = ft.Colors.GREEN
        ft.context.page.update()  # Second rafraîchissement visuel pour afficher le succès

    # --- RECONSTRUCTION DE L'ARBRE (DÉCLARATIF) ---

    return ft.Container(
        padding=30,
        expand=True,
        content=ft.Column(
            controls=cast(
                list[ft.Control],
                [
                    ft.Text(
                        "Synchronisation Google", size=26, weight=ft.FontWeight.BOLD
                    ),
                    ft.Button("Synchroniser avec Google", on_click=synchroniser),
                    ft.ProgressRing(
                        visible=state_progress_visible
                    ),  # État dynamique lue en temps réel
                    ft.Text(
                        state_message_value, color=state_message_color
                    ),  # Texte et couleur dynamiques
                ],
            )
        ),
    )
