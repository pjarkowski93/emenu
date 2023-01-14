from djmoney.contrib.django_rest_framework import MoneyField
from rest_framework import serializers

from emenu import models


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = "__all__"


class DishSerializer(serializers.ModelSerializer):
    price = MoneyField(max_digits=8, decimal_places=2)

    class Meta:
        model = models.Dish
        fields = "__all__"


class CreateMenuWithDishSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.MenuWithDish
        fields = "__all__"


class ReadMenuSerializer(serializers.Serializer):
    uuid = serializers.UUIDField()
    name = serializers.CharField()
    dishes = serializers.SerializerMethodField()

    def get_dishes(self, instance):
        dishes_uuids = instance.dishes.all().values_list("dish", flat=True)
        return DishSerializer(
            models.Dish.objects.filter(uuid__in=dishes_uuids), many=True
        ).data

    class Meta:
        model = models.Menu
        fields = ("uuid", "dishes")
