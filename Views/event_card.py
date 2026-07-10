import flet as ft

from Models import EventDTO


@ft.component
def EventCard(event: EventDTO):
    """
    Carte permettant d'afficher les informations d'un événement.

    Paramètre
    ---------
    event : EventDTO
        Objet contenant les données de l'événement.
    """

    # État local utilisé pour actualiser automatiquement l'interface.
    cours_id, set_cours_id = ft.use_state(event.cours_id)

    def modifier_nom(e):
        """
        Fonction appelée lorsque l'utilisateur clique sur le bouton.
        """

        nouvelle_valeur = 0

        # Mise à jour de l'objet DTO.
        event.cours_id = nouvelle_valeur

        # Mise à jour de l'état graphique.
        # Cette opération provoque automatiquement le nouveau rendu.
        set_cours_id(nouvelle_valeur)

    return ft.Container(
        padding=15,
        border_radius=10,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(
            blur_radius=8,
            color=ft.Colors.BLACK_12,
        ),
        content=ft.Column(
            spacing=8,
            controls=[
                ft.Text(
                    value=str(cours_id),
                    size=16,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Text(
                    value=f"Date : {event.date}",
                ),
                ft.Text(
                    value=f"Heure : {event.heure_debut}",
                ),
                ft.Text(
                    value=f"Salle : {event.salle}",
                ),
                ft.Text(
                    value=f"UE : {cours_id}",
                ),
                ft.Text(
                    value=f"Type : {event.types}",
                ),
                ft.Button(
                    content=ft.Text("Éditer"),
                    on_click=modifier_nom,
                ),
            ],
        ),
    )