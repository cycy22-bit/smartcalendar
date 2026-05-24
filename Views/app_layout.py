import flet as ft


class SidebarComponent:
    def build(self):
        return ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.icons.DASHBOARD,
                    label="Dashboard"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.CALENDAR_MONTH,
                    label="Calendrier"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.UPLOAD_FILE,
                    label="Import"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.FILTER_LIST,
                    label="Filtres"
                ),
                ft.NavigationRailDestination(
                    icon=ft.icons.SYNC,
                    label="Sync"
                ),
            ],
        )


class AppLayout(ft.Row):
    def __init__(self, content):
        super().__init__()

        self.controls = [
            SidebarComponent().build(),
            ft.VerticalDivider(width=1),
            ft.Container(content=content, expand=True)
        ]

        self.expand = True