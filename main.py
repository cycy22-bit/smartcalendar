import flet as ft

from Views.app_layout import AppLayout
from Views.calendrier_view import (
    AuthView,
    CalendarView,
    DashboardView,
    FilterView,
    ImportView,
    SyncView,
)

# --- COMPOSANTS DE ROUTE DÉCLARATIFS ---


@ft.component
def HomeRoute():
    def on_connexion_click(e):
        ft.context.page.navigate("/login")
        ft.context.page.update()

    return ft.Container(
        expand=True,
        alignment=ft.Alignment.CENTER,
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            controls=[
                ft.Text("Bienvenue sur SmartCalendrier", size=30),
                ft.Button(
                    "Connexion",
                    on_click=on_connexion_click,
                ),
            ],
        ),
    )


@ft.component
def LoginRoute():
    return AuthView()


@ft.component
def DashboardRoute():
    return AppLayout(DashboardView())


@ft.component
def CalendrierRoute():
    return AppLayout(CalendarView())


@ft.component
def ImportRoute():
    return AppLayout(ImportView())


@ft.component
def FiltresRoute():
    return AppLayout(FilterView())


@ft.component
def SyncRoute():
    return AppLayout(SyncView())


# --- APPLICATION GLOBALE (Nécessaire pour le contexte du Router) ---


@ft.component
def App():
    # Le Router vit désormais en toute sécurité à l'intérieur d'un composant @ft.component
    return ft.Router(
        manage_views=True,
        routes=[
            ft.Route(index=True, component=HomeRoute),
            ft.Route(path="login", component=LoginRoute),
            ft.Route(path="dashboard", component=DashboardRoute),
            ft.Route(path="calendrier", component=CalendrierRoute),
            ft.Route(path="import", component=ImportRoute),
            ft.Route(path="filtres", component=FiltresRoute),
            ft.Route(path="sync", component=SyncRoute),
        ],
    )


# --- POINT D'ENTRÉE IMPÉRATIF ---


async def main(page: ft.Page):
    page.title = "SmartCalendrier"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1000
    page.window.height = 700

    page.render(App)


if __name__ == "__main__":
    ft.run(main)
