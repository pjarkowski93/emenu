from django.db.models import Count
from django_filters import rest_framework as rest_filters

from emenu.models import Dish, Menu


class MenuFilter(rest_filters.FilterSet):
    name = rest_filters.CharFilter()
    created_at_lte = rest_filters.Filter(field_name="created_at", lookup_expr="lte")
    created_at_gt = rest_filters.Filter(field_name="created_at", lookup_expr="gt")
    updated_at_lte = rest_filters.Filter(field_name="updated_at", lookup_expr="lte")
    updated_at_gt = rest_filters.Filter(field_name="updated_at", lookup_expr="gt")
    dish_count = rest_filters.Filter(method="filter_by_dish_count")

    def filter_by_dish_count(self, queryset, name, value):
        return (
            queryset.prefetch_related("dishes")
            .annotate(dish_count=Count("dishes"))
            .filter(dish_count__gte=value)
        )

    class Meta:
        model = Menu
        fields = (
            "name",
            "dish_count",
            "created_at_lte",
            "created_at_gt",
            "updated_at_lte",
            "updated_at_gt",
        )


class DishFilter(rest_filters.FilterSet):
    name = rest_filters.CharFilter()
    price_lte = rest_filters.Filter(field_name="price", lookup_expr="lte")
    price_gt = rest_filters.Filter(field_name="price", lookup_expr="gt")
    preparing_time_lte = rest_filters.Filter(
        field_name="preparing_time", lookup_expr="lte"
    )
    preparing_time_gt = rest_filters.Filter(
        field_name="preparing_time", lookup_expr="gt"
    )
    is_vegetarian = rest_filters.BooleanFilter()
    created_at_lte = rest_filters.Filter(field_name="created_at", lookup_expr="lte")
    created_at_gt = rest_filters.Filter(field_name="created_at", lookup_expr="gt")
    updated_at_lte = rest_filters.Filter(field_name="updated_at", lookup_expr="lte")
    updated_at_gt = rest_filters.Filter(field_name="updated_at", lookup_expr="gt")

    class Meta:
        model = Dish
        fields = (
            "name",
            "price_lte",
            "price_gt",
            "preparing_time_lte",
            "preparing_time_gt",
            "created_at_lte",
            "created_at_gt",
            "updated_at_lte",
            "updated_at_gt",
        )
