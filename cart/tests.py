from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from .models import Cart, Item
from products.models import Category, Product


class CartAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="cart-user",
            email="cart-user@example.com",
            password="safe-password-123",
        )
        category = Category.objects.create(name="Books", slug="books")
        self.product = Product.objects.create(
            name="Cart Product",
            description="A test product",
            slug="cart-product",
            price="9.99",
            stock=3,
            category=category,
        )

    def test_cart_requires_authentication(self):
        response = self.client.get("/api/v1/cart/")

        self.assertEqual(response.status_code, 401)

    def test_adding_item_accumulates_quantity(self):
        self.client.force_authenticate(self.user)

        first = self.client.post(
            "/api/v1/cart/items/add/",
            {"product_id": self.product.id, "quantity": 1},
            format="json",
        )
        second = self.client.post(
            "/api/v1/cart/items/add/",
            {"product_id": self.product.id, "quantity": 2},
            format="json",
        )

        self.assertEqual(first.status_code, 200)
        self.assertEqual(second.status_code, 200)
        item = Item.objects.get(cart__user=self.user, product=self.product)
        self.assertEqual(item.quantity, 3)

    def test_cart_rejects_quantity_above_stock(self):
        self.client.force_authenticate(self.user)

        response = self.client.post(
            "/api/v1/cart/items/add/",
            {"product_id": self.product.id, "quantity": 4},
            format="json",
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(Item.objects.filter(cart__user=self.user).exists())

    def test_deleting_item_only_affects_current_users_cart(self):
        other_user = get_user_model().objects.create_user(
            username="other-user",
            email="other@example.com",
            password="safe-password-123",
        )
        own_cart = Cart.objects.create(user=self.user)
        other_cart = Cart.objects.create(user=other_user)
        own_item = Item.objects.create(cart=own_cart, product=self.product, quantity=1)
        Item.objects.create(cart=other_cart, product=self.product, quantity=1)
        self.client.force_authenticate(self.user)

        response = self.client.delete(f"/api/v1/cart/items/delete/{self.product.id}")

        self.assertEqual(response.status_code, 204)
        self.assertFalse(Item.objects.filter(pk=own_item.pk).exists())
        self.assertTrue(
            Item.objects.filter(cart=other_cart, product=self.product).exists()
        )
