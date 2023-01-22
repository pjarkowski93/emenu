import logging

from notification.enums import NotificationTypes
from notification.exceptions import LackOfSenderException
from notification.models import Notification
from notification.tasks import send_email

logger = logging.getLogger(__name__)


class SenderManager:
    def __init__(self, notification: Notification) -> None:
        self.notification = notification

    @property
    def sender(self):
        if self.notification.template.type == NotificationTypes.EMAIL.name:
            return send_email
        raise LackOfSenderException(
            "Sender for the message type "
            f"({self.notification.template.type}) does not exist."
        )

    def send(self) -> None:
        self.sender.apply_async(
            (),
            {"notification_uuid": self.notification.uuid},
        )
