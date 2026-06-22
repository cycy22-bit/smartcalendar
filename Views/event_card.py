import flet as ft

from Models import EventDTO

# # TODO : Add EventDTO Name


# class EventCard(ft.Container):
#     def __init__(self, event: EventDTO):
#         super().__init__()

#         self.event_data = event

#         self.nom_text = ft.Text(
#             f"{self.event_data.cours_id}", size=16, weight=ft.FontWeight.BOLD
#         )

#         self.buton = ft.Button(
#             content=ft.Text("Éditer (Test)"), on_click=self.modifier_nom
#         )

#         self.content = ft.Column(
#             controls=[
#                 self.nom_text,
#                 ft.Text(f"Date : {self.event_data.date}"),
#                 ft.Text(f"Heure : {self.event_data.heure_debut}"),
#                 ft.Text(f"Salle : {self.event_data.salle}"),
#                 ft.Text(f"UE : {self.event_data.cours_id}"),  # TODO : Add EventDTO Name
#                 ft.Text(f"Type : {self.event_data.types}"),
#                 self.buton,
#             ]
#         )

#         self.padding = 15
#         self.border_radius = 10
#         self.bgcolor = ft.Colors.WHITE
#         self.shadow = ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK_12)

#     def modifier_nom(self, e):
#         self.event_data.cours_id = 0  # TODO : Add EventDTO Name
#         self.nom_text.value = f"{self.event_data.cours_id}"
#         self.nom_text.update()


# import flet as ft

# from Models import EventDTO

# # TODO : Add EventDTO Name


# class EventCard(ft.Container):
#     def __init__(self, event: EventDTO):
#         super().__init__()

#         self.event_data = event

#         # On garde une référence sur la colonne pour pouvoir manipuler sa liste de contrôles
#         self.layout_column = ft.Column()

#         # On crée le composant de texte initial
#         self.nom_text = ft.Text(
#             f"{self.event_data.cours_id}", size=16, weight=ft.FontWeight.BOLD
#         )

#         self.buton = ft.Button(
#             content=ft.Text("Éditer (Test)"), on_click=self.modifier_nom
#         )

#         # Remplissage initial de la colonne
#         self.layout_column.controls = [
#             self.nom_text,
#             ft.Text(f"Date : {self.event_data.date}"),
#             ft.Text(f"Heure : {self.event_data.heure_debut}"),
#             ft.Text(f"Salle : {self.event_data.salle}"),
#             ft.Text(f"UE : {self.event_data.cours_id}"),  # TODO : Add EventDTO Name
#             ft.Text(f"Type : {self.event_data.types}"),
#             self.buton,
#         ]

#         # Assigner la colonne comme contenu du Container principal
#         self.content = self.layout_column

#         self.padding = 15
#         self.border_radius = 10
#         self.bgcolor = ft.Colors.WHITE
#         self.shadow = ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK_12)

#     def modifier_nom(self, e):
#         # 1. Mise à jour de la donnée (Model)
#         self.event_data.cours_id = 0  # TODO : Add EventDTO Name

#         # 2. Création d'une NOUVELLE instance de texte (évite le conflit du contrôle gelé)
#         self.nom_text = ft.Text(
#             f"{self.event_data.cours_id}", size=16, weight=ft.FontWeight.BOLD
#         )

#         # 3. Remplacement du premier élément (index 0) dans la liste des contrôles
#         self.layout_column.controls[0] = self.nom_text

#         # 4. Mise à jour de la colonne uniquement (le layout accepte le changement de sa liste de contrôles)
#         self.layout_column.update()


# TODO : Add EventDTO Name


# class EventCard(ft.Container):
#     def __init__(self, event: EventDTO):
#         super().__init__()

#         # On stocke uniquement les données dans le constructeur
#         self.event_data = event

#         # Configuration des styles de la carte (autorisé dans __init__)
#         self.padding = 15
#         self.border_radius = 10
#         self.bgcolor = ft.Colors.WHITE
#         self.shadow = ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK_12)

#         # def build(self):
#         #     """
#         #     CONVENTION POO NATIVE DE FLET :
#         #     Flet appelle automatiquement cette méthode au premier affichage ET
#         #     à chaque fois que page.update() est demandé.
#         #     Ici, les contrôles sont générés dynamiquement sans jamais être bloqués (frozen).
#         #     """
#         self.content = ft.Column(
#             controls=[
#                 # Le texte lit directement la valeur en temps réel
#                 ft.Text(
#                     f"{self.event_data.cours_id}", size=16, weight=ft.FontWeight.BOLD
#                 ),
#                 ft.Text(f"Date : {self.event_data.date}"),
#                 ft.Text(f"Heure : {self.event_data.heure_debut}"),
#                 ft.Text(f"Salle : {self.event_data.salle}"),
#                 ft.Text(f"UE : {self.event_data.cours_id}"),  # TODO : Add EventDTO Name
#                 ft.Text(f"Type : {self.event_data.types}"),
#                 ft.Button(content=ft.Text("Éditer (Test)"), on_click=self.modifier_nom),
#             ]
#         )

#     def modifier_nom(self, e):
#         # 1. On modifie la donnée pure
#         self.event_data.cours_id = 0  # TODO : Add EventDTO Name

#         # 2. On demande à la page globale de se rafraîchir.
#         # Flet va ré-exécuter proprement la méthode build() ci-dessus pour redessiner la carte.
#         self.page.update()


@ft.component
def EventCard(event: EventDTO):
    # Cette fonction interne intercepte le clic, modifie la donnée (Model)
    # et demande un rafraîchissement global via ft.context.page
    def modifier_nom(e):
        event.cours_id = 0  # TODO : Add EventDTO Name
        ft.context.page.update()  # Déclenche la reconstruction propre de l'arbre graphique

    # L'arbre complet est retourné de manière déclarative à chaque mise à jour
    return ft.Container(
        padding=15,
        border_radius=10,
        bgcolor=ft.Colors.WHITE,
        shadow=ft.BoxShadow(blur_radius=8, color=ft.Colors.BLACK_12),
        content=ft.Column(
            controls=[
                # Les textes évaluent la valeur en temps réel à chaque re-rendu
                ft.Text(f"{event.cours_id}", size=16, weight=ft.FontWeight.BOLD),
                ft.Text(f"Date : {event.date}"),
                ft.Text(f"Heure : {event.heure_debut}"),
                ft.Text(f"Salle : {event.salle}"),
                ft.Text(f"UE : {event.cours_id}"),  # TODO : Add EventDTO Name
                ft.Text(f"Type : {event.types}"),
                ft.Button(content=ft.Text("Éditer (Test)"), on_click=modifier_nom),
            ]
        ),
    )
