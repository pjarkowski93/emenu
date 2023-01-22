from django.core.management.base import BaseCommand

from notification.utils import send_notification


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        send_notification()
