from django.urls import path
from rest_framework import routers

from emenu import views

router = routers.DefaultRouter()
router.register("dish", views.DishViewSet, basename="dish")
router.register("menu", views.MenuViewSet, basename="menu")


urlpatterns = [
    path(
        "add_dish_to_menu/",
        views.AddDishToMenuView.as_view(),
        name="add_dish_to_menu",
    ),
    path(
        "add_dish_to_menu/<uuid:uuid>",
        views.UpdateDestoryDishMenuView.as_view(),
        name="update_destroy_dish_menu",
    ),
] + router.urls
