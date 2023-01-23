from django.core.management.base import BaseCommand

from notification.utils import create_update_dish_notification


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        create_update_dish_notification()
