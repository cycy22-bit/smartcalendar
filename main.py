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

# --- WRAPPERS DYNAMIQUES POUR LE ROUTER ---
# Ces fonctions forcent Flet à recréer une nouvelle instance mutable de vos classes POO à chaque accès.


@ft.component
def HomeRoute():
    return ft.View(
        route="/",
        controls=[
            ft.Container(
                expand=True,
                alignment=ft.Alignment.CENTER,
                content=ft.Column(
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Bienvenue sur SmartCalendrier", size=30),
                        ft.Button(
                            "Connexion",
                            on_click=lambda e: ft.context.page.navigate("/login"),
                        ),
                    ],
                ),
            )
        ],
    )


@ft.component
def LoginRoute():
    return ft.View(route="/login", controls=[AuthView()])


@ft.component
def DashboardRoute():
    return ft.View(route="/dashboard", controls=[AppLayout(DashboardView())])


@ft.component
def CalendrierRoute():
    # Recrée dynamiquement CalendarView() pour qu'il soit modifiable
    return ft.View(route="/calendrier", controls=[AppLayout(CalendarView())])


@ft.component
def ImportRoute():
    return ft.View(route="/import", controls=[AppLayout(ImportView())])


@ft.component
def FilterRoute():
    return ft.View(route="/filtres", controls=[AppLayout(FilterView())])


@ft.component
def SyncRoute():
    return ft.View(route="/sync", controls=[AppLayout(SyncView())])


# --- APPLICATION GLOBALE ---


@ft.component
def App():
    return ft.Router(
        manage_views=True,
        routes=[
            ft.Route(path="/", component=HomeRoute),
            ft.Route(path="/login", component=LoginRoute),
            ft.Route(path="/dashboard", component=DashboardRoute),
            ft.Route(path="/calendrier", component=CalendrierRoute),
            ft.Route(path="/import", component=ImportRoute),
            ft.Route(path="/filtres", component=FilterRoute),
            ft.Route(path="/sync", component=SyncRoute),
        ],
    )


# --- POINT D'ENTRÉE ---


async def main(page: ft.Page):
    page.title = "SmartCalendrier"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window.width = 1000
    page.window.height = 700

    # Rendu initial de l'application via les vues gérées par le routeur
    page.render_views(App)


if __name__ == "__main__":
    ft.run(main)
