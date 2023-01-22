from notification.enums import NotificationStatuses
from notification.models import Notification
from notification.sender_manager import SenderManager


def send_notification() -> None:
    notifications = Notification.objects.filter(
        status=NotificationStatuses.CREATED.name
    )
    for notification in notifications:
        sender_manager = SenderManager(notification=notification)
        sender_manager.send()
