import logging
from uuid import UUID

from celery import shared_task, Task
from django.contrib.auth import get_user_model

from notification.email import EmailSender
from notification.enums import NotificationStatuses
from notification.models import Notification
from notification.notification_common import get_email_data

logger = logging.getLogger(__name__)

User = get_user_model()


class NotificationTask(Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        notification = Notification.objects.filter(uuid=kwargs["notification_uuid"])
        message = notification[0].get_message(message_data=get_email_data())
        notification.update(
            sent_message=message,
            error_message=exc,
            status=NotificationStatuses.FAILED.name,
        )

    def on_success(self, retval, task_id, args, kwargs):
        notification = Notification.objects.filter(uuid=kwargs["notification_uuid"])
        message = notification[0].get_message(message_data=get_email_data())
        notification.update(
            sent_message=message,
            status=NotificationStatuses.SENT.name,
        )


@shared_task(base=NotificationTask)
def send_email(notification_uuid: UUID) -> None:
    notification = Notification.objects.get(uuid=notification_uuid)
    message = notification.get_message(message_data=get_email_data())
    email_sender = EmailSender()
    email_sender.send(
        message=message,
        title=notification.title,
        recipient_email=notification.recipient.email,
    )
