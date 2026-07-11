from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase

from cart.models import Cart, Item
from products.models import Category, Product


class CheckoutAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="shopper", email="shopper@example.com", password="safe-password-123"
        )
        category = Category.objects.create(name="Books", slug="books")
        self.product = Product.objects.create(
            name="Django for Shops",
            description="A test product",
            slug="django-for-shops",
            price="12.50",
            stock=3,
            category=category,
        )
        cart = Cart.objects.create(user=self.user)
        Item.objects.create(cart=cart, product=self.product, quantity=2)
        self.client.force_authenticate(self.user)

    def test_checkout_creates_order_and_deducts_stock(self):
        response = self.client.post("/api/v1/orders/checkout/", format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["total_price"], "25.00")
        self.assertEqual(len(response.data["items"]), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 1)

    def test_checkout_rejects_insufficient_stock(self):
        Item.objects.filter(cart__user=self.user).update(quantity=4)

        response = self.client.post("/api/v1/orders/checkout/", format="json")

        self.assertEqual(response.status_code, 400)
        self.product.refresh_from_db()
        self.assertEqual(self.product.stock, 3)

    def test_order_list_only_returns_current_users_orders(self):
        self.client.post("/api/v1/orders/checkout/", format="json")

        response = self.client.get("/api/v1/orders/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
