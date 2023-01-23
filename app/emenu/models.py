import logging
from datetime import datetime, timedelta
from uuid import uuid4

from django.db import models
from djmoney.models.fields import MoneyField

from notification.exceptions import LackOfMessageDataException

logger = logging.getLogger(__name__)


class Menu(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=100, blank=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "menu"


class Dish(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    name = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    price = MoneyField(max_digits=8, decimal_places=2, default_currency="PLN")
    preparing_time = models.PositiveIntegerField(help_text="Preparing time in minutes")
    is_vegetarian = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dish"

    @staticmethod
    def _get_year_month_yesterday() -> tuple[int, int, int]:
        yesterday_datetime = datetime.today() - timedelta(days=1)
        year = yesterday_datetime.year
        month = yesterday_datetime.month
        day = yesterday_datetime.day
        return year, month, day

    @staticmethod
    def is_data_to_send() -> bool:
        year, month, day = Dish._get_year_month_yesterday()
        return Dish.objects.filter(
            models.Q(
                created_at__year=year, created_at__month=month, created_at__day=day
            )
            | models.Q(
                updated_at__year=year, updated_at__month=month, updated_at__day=day
            )
        ).exists()

    @staticmethod
    def get_notification_dishes() -> models.QuerySet:
        if not Dish.is_data_to_send():
            logger.info("Nothing to send.")
            raise LackOfMessageDataException("Nothing to send.")
        year, month, day = Dish._get_year_month_yesterday()
        return Dish.objects.filter(
            models.Q(
                created_at__year=year, created_at__month=month, created_at__day=day
            )
            | models.Q(
                updated_at__year=year, updated_at__month=month, updated_at__day=day
            )
        )


class MenuDishMap(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="dishes")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="menu")

    class Meta:
        db_table = "menu_dish_map"
        unique_together = ("menu", "dish")
