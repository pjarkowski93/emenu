from emenu.notifications.notification_common import NotificationSender


class SenderManager:
    def __init__(self, notification_sender: NotificationSender, message: str) -> None:
        self.notification_sender = notification_sender
        self.message = message

    def send(self, recipient_email: str) -> None:
        self.notification_sender.send(
            message=self.message, recipient_email=recipient_email
        )
