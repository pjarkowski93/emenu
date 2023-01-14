from django_filters import rest_framework as rest_filters
from rest_framework import generics, viewsets

from emenu import models, serializers


class MenuViewSet(viewsets.ModelViewSet):
    queryset = models.Menu.objects.filter(dishes__isnull=False)
    serializer_class = serializers.MenuSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]
    lookup_field = "uuid"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.ReadMenuSerializer
        return serializers.MenuSerializer


class DishViewSet(viewsets.ModelViewSet):
    queryset = models.Dish.objects.all()
    serializer_class = serializers.DishSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]
    lookup_field = "uuid"


class AddDishToMenuViewSet(
    generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView
):
    queryset = models.MenuWithDish.objects.all()
    serializer_class = serializers.CreateMenuWithDishSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]
    lookup_field = "uuid"
