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


async def main(page: ft.Page):
    page.title = "SmartCalendrier"
    page.theme_mode = ft.ThemeMode.LIGHT
    # set window size width to 1000 and height to 700
    page.window.width = 1000
    page.window.height = 700

    # ROUTAGE
    def route_change(route):
        page.views.clear()

        if page.route == "/":
            page.views.append(
                ft.View(
                    route="/",
                    controls=[
                        AppLayout(
                            ft.Container(
                                expand=True,
                                alignment=ft.Alignment.CENTER,
                                content=ft.Column(
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                    controls=[
                                        ft.Text(
                                            "Bienvenue sur SmartCalendrier", size=30
                                        ),
                                        ft.Button(
                                            "Connexion",
                                            on_click=lambda e: page.go("/login"),
                                        ),
                                    ],
                                ),
                            )
                        )
                    ],
                )
            )

        elif page.route == "/login":
            page.views.append(ft.View(route="/login", controls=[AuthView()]))

        elif page.route == "/dashboard":
            page.views.append(
                ft.View(route="/dashboard", controls=[AppLayout(DashboardView())])
            )

        elif page.route == "/calendrier":
            page.views.append(
                ft.View(route="/calendrier", controls=[AppLayout(CalendarView())])
            )

        elif page.route == "/import":
            page.views.append(
                ft.View(route="/import", controls=[AppLayout(ImportView())])
            )

        elif page.route == "/filtres":
            page.views.append(
                ft.View(route="/filtres", controls=[AppLayout(FilterView())])
            )

        elif page.route == "/sync":
            page.views.append(ft.View(route="/sync", controls=[AppLayout(SyncView())]))

        page.update()

    # NAVIGATION RETOUR
    async def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # DÉMARRAGE
    await page.push_route("/")


if __name__ == "__main__":
    ft.run(main)
