from uuid import uuid4
from parameterized import parameterized
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from model_bakery import baker
from rest_framework.test import APIClient

from emenu.models import Dish


class DishViewSetTestCase(TestCase):
    def setUp(self) -> None:
        baker.generators.add("djmoney.models.fields.MoneyField", lambda: "100.00")
        self.api_client = APIClient()
        User = get_user_model()
        self.user = User.objects.create_user(
            "test_user", "test_user@email.com", "testuser123"
        )
        self.dish_list_url = reverse("dish-list")

    def test_create_dish(self):
        self.api_client.force_authenticate(user=self.user)
        data_to_create = {
            "name": "dish name",
            "description": "dish description",
            "price": 100.00,
            "preparing_time": 40,
            "is_vegetarian": True,
        }
        response = self.api_client.post(
            self.dish_list_url, data=data_to_create, format="json"
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["name"], data_to_create["name"])
        self.assertEqual(response.data["description"], data_to_create["description"])
        self.assertEqual(response.data["price"], f"{data_to_create['price']:.2f}")
        self.assertEqual(
            response.data["preparing_time"], data_to_create["preparing_time"]
        )
        self.assertEqual(
            response.data["is_vegetarian"], data_to_create["is_vegetarian"]
        )

    def test_get_list_dish(self):
        dish1 = baker.make(Dish)
        dish2 = baker.make(Dish)
        response = self.api_client.get(self.dish_list_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]["uuid"], str(dish1.uuid))
        self.assertEqual(response.data[1]["uuid"], str(dish2.uuid))

    def test_get_single_dish(self):
        dish = baker.make(Dish)
        baker.make(Dish)
        dish_detail_url = reverse("dish-detail", kwargs={"uuid": str(dish.uuid)})
        response = self.api_client.get(dish_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["uuid"], str(dish.uuid))

    def test_put_dish(self):
        self.api_client.force_authenticate(user=self.user)
        dish = baker.make(Dish)
        data_to_update = {
            "uuid": str(dish.uuid),
            "name": "new name",
            "description": dish.description,
            "price": 20.00,
            "preparing_time": dish.preparing_time,
            "is_vegetarian": dish.is_vegetarian,
            "created_at": dish.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            "updated_at": dish.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
        }
        dish_detail_url = reverse("dish-detail", kwargs={"uuid": str(dish.uuid)})
        response = self.api_client.put(
            dish_detail_url, data=data_to_update, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["uuid"], str(dish.uuid))
        self.assertNotEqual(response.data["name"], dish.name)
        self.assertNotEqual(response.data["name"], f"{dish.price.amount}:.2f")
        self.assertNotEqual(response.data["updated_at"], data_to_update["updated_at"])
        self.assertEqual(response.data["name"], data_to_update["name"])
        self.assertEqual(response.data["description"], data_to_update["description"])
        self.assertEqual(response.data["price"], f"{data_to_update['price']:.2f}")
        self.assertEqual(
            response.data["preparing_time"], data_to_update["preparing_time"]
        )
        self.assertEqual(
            response.data["is_vegetarian"], data_to_update["is_vegetarian"]
        )
        self.assertEqual(response.data["created_at"], data_to_update["created_at"])

    def test_patch_dish(self):
        self.api_client.force_authenticate(user=self.user)
        dish = baker.make(Dish)
        data_to_update = {
            "name": "new name",
        }
        dish_detail_url = reverse("dish-detail", kwargs={"uuid": str(dish.uuid)})
        response = self.api_client.patch(
            dish_detail_url, data=data_to_update, format="json"
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["name"], data_to_update["name"])

    def test_delete_dish(self):
        self.api_client.force_authenticate(user=self.user)
        dish = baker.make(Dish)
        dish_detail_url = reverse("dish-detail", kwargs={"uuid": str(dish.uuid)})
        response = self.api_client.delete(dish_detail_url)

        self.assertEqual(response.status_code, 204)

        response = self.api_client.delete(dish_detail_url)

        self.assertEqual(response.status_code, 404)

    def test_not_existing_dish(self):
        dish_detail_url = reverse("dish-detail", kwargs={"uuid": str(uuid4())})
        response = self.api_client.get(dish_detail_url)

        self.assertEqual(response.status_code, 404)

    @parameterized.expand(("post", "patch", "put", "delete"))
    def test_unauthorized_requests(self, method):
        url = reverse("dish-detail", kwargs={"uuid": str(uuid4())})
        if method == "post":
            url = self.dish_list_url

        request_method = getattr(self.api_client, method)
        response = request_method(url)

        self.assertEqual(response.status_code, 401)
