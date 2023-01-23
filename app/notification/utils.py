import logging

from django.contrib.auth import get_user_model

from emenu.models import Dish
from notification.enums import NotificationStatuses
from notification.models import Notification, NotificationTemplate
from notification.sender_manager import SenderManager

logger = logging.getLogger(__name__)


def send_notification() -> None:
    notifications = Notification.objects.filter(
        status=NotificationStatuses.CREATED.name
    )
    for notification in notifications:
        sender_manager = SenderManager(notification=notification)
        sender_manager.send()


def create_update_dish_notification() -> None:
    if not Dish.is_data_to_send():
        logger.info("Nothing to send.")
        return
    User = get_user_model()
    email_template = NotificationTemplate.objects.get(name="Email message template")
    for user in User.objects.all():
        Notification.objects.create(
            template=email_template, recipient=user, title="Dishes update"
        )
