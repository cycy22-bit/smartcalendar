import time


class NotifyService:
    def send_notification(self, message: str):
        print(f"[NOTIFICATION] {message}")

    def simulate_sync(self):
        print("Synchronisation en cours...")
        time.sleep(2)
        print("Synchronisation terminée.")

    def get_notifications(self):
        return [
            "Cours de Math à 08h",
            "TP Electronique à 10h",
            "Réunion projet à 14h"
        ]