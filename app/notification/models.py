from uuid import uuid4

from django.contrib.auth import get_user_model
from django.db import models

from notification.enums import NotificationStatuses, NotificationTypes

User = get_user_model()


class NotificationTemplate(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=200, unique=True)
    message_template = models.TextField(
        help_text="Message template written in python string format"
    )
    type = models.CharField(max_length=20, choices=NotificationTypes.choices())
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notification_template"


class Notification(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    template = models.ForeignKey(NotificationTemplate, on_delete=models.DO_NOTHING)
    status = models.CharField(
        max_length=20,
        choices=NotificationStatuses.choices(),
        default=NotificationStatuses.CREATED.name,
    )
    recipient = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    sent_message = models.TextField(blank=True)
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "notification"

    def get_message(self, message_data: dict[str, str]) -> str:
        return self.template.message_template.format(**message_data)
