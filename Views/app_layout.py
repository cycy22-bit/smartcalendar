import flet as ft
from typing import cast
# class SidebarComponent:
#     def build(self):
#         return ft.NavigationRail(
#             selected_index=0,
#             label_type=ft.NavigationRailLabelType.ALL,
#             destinations=[
#                 ft.NavigationRailDestination(
#                     icon=ft.Icons.DASHBOARD, label="Dashboard"
#                 ),
#                 ft.NavigationRailDestination(
#                     icon=ft.Icons.CALENDAR_MONTH, label="Calendrier"
#                 ),
#                 ft.NavigationRailDestination(icon=ft.Icons.UPLOAD_FILE, label="Import"),
#                 ft.NavigationRailDestination(
#                     icon=ft.Icons.FILTER_LIST, label="Filtres"
#                 ),
#                 ft.NavigationRailDestination(icon=ft.Icons.SYNC, label="Sync"),
#             ],
#         )


# class AppLayout(ft.Row):
#     def __init__(self, content):
#         super().__init__()

#         self.controls = [
#             SidebarComponent().build(),
#             ft.VerticalDivider(width=1),
#             ft.Container(content=content, expand=True),
#         ]

#         self.expand = True


# Dictionnaire de correspondance entre les index de la barre et les URLs
ROUTES_MAP = {
    0: "/dashboard",
    1: "/calendrier",
    2: "/import",
    3: "/filtres",
    4: "/sync",
}


class SidebarComponent(ft.NavigationRail):
    def __init__(self, page: ft.Page):
        # Initialisation de la classe parente ft.NavigationRail
        super().__init__()

        self.page_ref = page
        self.label_type = ft.NavigationRailLabelType.ALL
        self.on_change = self.navigation_changed

        # Déterminer automatiquement l'onglet actif selon l'URL de la page
        self.selected_index = 0
        for index, route in ROUTES_MAP.items():
            if self.page_ref.route == route:
                self.selected_index = index
                break

        # Liste des destinations de la barre latérale
        self.destinations = [
            ft.NavigationRailDestination(icon=ft.Icons.DASHBOARD, label="Dashboard"),
            ft.NavigationRailDestination(
                icon=ft.Icons.CALENDAR_MONTH, label="Calendrier"
            ),
            ft.NavigationRailDestination(icon=ft.Icons.UPLOAD_FILE, label="Import"),
            ft.NavigationRailDestination(icon=ft.Icons.FILTER_LIST, label="Filtres"),
            ft.NavigationRailDestination(icon=ft.Icons.SYNC, label="Sync"),
        ]

    def navigation_changed(self, e):
        # Récupère l'URL cible associée au bouton cliqué
        target_route = ROUTES_MAP.get(cast(int, self.selected_index), "/dashboard")

        # Redirection via l'objet page
        self.page_ref.navigate(target_route)
        self.page_ref.update()


class AppLayout(ft.Row):
    def __init__(self, content):
        # Initialisation de la classe parente ft.Row
        super().__init__()

        self.expand = True

        # Accès à la page globale depuis le contexte actuel de Flet
        page = ft.context.page

        # Remplissage direct des contrôles dans le constructeur
        self.controls = [
            SidebarComponent(page),  # Injection de la page pour piloter les routes
            ft.VerticalDivider(width=1),
            ft.Container(content=content, expand=True),
        ]
