from uuid import UUID
from django_filters import rest_framework as rest_filters
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from emenu import models, serializers
from emenu.filters import DishFilter, MenuFilter


class MenuViewSet(viewsets.ModelViewSet):
    queryset = models.Menu.objects.filter(dishes__isnull=False)
    serializer_class = serializers.MenuSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]
    filterset_class = MenuFilter
    lookup_field = "uuid"

    def get_serializer_class(self):
        if self.request.method == "GET":
            return serializers.ReadMenuSerializer
        return serializers.MenuSerializer

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method == "GET":
            self.permission_classes = []
        return super().get_permissions()

    @action(methods=["GET"], detail=True)
    def menu_details(self, request, *args, **kwargs):
        menu: models.Menu = self.get_object()
        return Response(serializers.ReadMenuDetailSerializer(menu).data)


class DishViewSet(viewsets.ModelViewSet):
    queryset = models.Dish.objects.all()
    serializer_class = serializers.DishSerializer
    filter_backends = [rest_filters.DjangoFilterBackend]
    filterset_class = DishFilter
    lookup_field = "uuid"

    def get_permissions(self):
        self.permission_classes = [IsAuthenticated]
        if self.request.method == "GET":
            self.permission_classes = []
        return super().get_permissions()


class AddDishToMenuViewSet(
    generics.CreateAPIView, generics.UpdateAPIView, generics.DestroyAPIView
):
    queryset = models.MenuDishMap.objects.all()
    serializer_class = serializers.CreateMenuDishMapSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [rest_filters.DjangoFilterBackend]
    lookup_field = "uuid"
