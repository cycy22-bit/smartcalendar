import flet as ft


class SidebarComponent:
    def build(self):
        return ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.DASHBOARD, label="Dashboard"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.CALENDAR_MONTH, label="Calendrier"
                ),
                ft.NavigationRailDestination(icon=ft.Icons.UPLOAD_FILE, label="Import"),
                ft.NavigationRailDestination(
                    icon=ft.Icons.FILTER_LIST, label="Filtres"
                ),
                ft.NavigationRailDestination(icon=ft.Icons.SYNC, label="Sync"),
            ],
        )


class AppLayout(ft.Row):
    def __init__(self, content):
        super().__init__()

        self.controls = [
            SidebarComponent().build(),
            ft.VerticalDivider(width=1),
            ft.Container(content=content, expand=True),
        ]

        self.expand = True
