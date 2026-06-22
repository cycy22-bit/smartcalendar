import flet as ft

from Views.app_layout import AppLayout
from Views.calendrier_view import CalendarView, AuthView, DashboardView, ImportView, FilterView, SyncView


def main(page: ft.Page):
    page.title = "SmartCalendrier"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_width = 1000
    page.window_height = 700

    # ROUTAGE
    def route_change(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        ft.Container(
                            expand=True,
                            alignment=ft.alignment.center,
                            content=ft.Column(
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                controls=[
                                    ft.Text("Bienvenue sur SmartCalendrier", size=30),
                                    ft.ElevatedButton(
                                        "Connexion",
                                        on_click=lambda e: page.go("/login")
                                    )
                                ]
                            )
                        )
                    ]
                )
            )

        elif page.route == "/login":
            page.views.append(
                ft.View("/login", controls=[AuthView()])
            )

        elif page.route == "/dashboard":
            page.views.append(
                ft.View("/dashboard", controls=[AppLayout(DashboardView())])
            )

        elif page.route == "/calendrier":
            page.views.append(
                ft.View("/calendrier", controls=[AppLayout(CalendarView())])
            )

        elif page.route == "/import":
            page.views.append(
                ft.View("/import", controls=[AppLayout(ImportView())])
            )

        elif page.route == "/filtres":
            page.views.append(
                ft.View("/filtres", controls=[AppLayout(FilterView())])
            )

        elif page.route == "/sync":
            page.views.append(
                ft.View("/sync", controls=[AppLayout(SyncView())])
            )

        page.update()

    # NAVIGATION RETOUR
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # DÉMARRAGE
    page.go("/")


if __name__ == "__main__":
    ft.app(target=main)