from uuid import uuid4

from django.db import models
from djmoney.models.fields import MoneyField


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
    preparing_time = models.IntegerField(help_text="Preparing time in minutes")
    is_vegetarian = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "dish"


class MenuWithDish(models.Model):
    uuid = models.UUIDField(default=uuid4, primary_key=True)
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="dishes")
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE, related_name="menu")

    class Meta:
        db_table = "menu_with_dish"
        unique_together = ("menu", "dish")
