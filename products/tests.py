from rest_framework.test import APITestCase

from .models import Category, Product


class CatalogAPITests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Books", slug="books")
        self.product = Product.objects.create(
            name="Django Basics",
            description="A public product",
            slug="django-basics",
            price="10.00",
            stock=5,
            category=self.category,
        )

    def test_anonymous_user_can_list_products(self):
        response = self.client.get("/api/v1/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"][0]["name"], self.product.name)

    def test_user_can_see_product_detail(self):
        response = self.client.get(f"/api/v1/products/{self.product.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], self.product.id)

    def test_category_endpoint_returns_category_products(self):
        response = self.client.get(f"/api/v1/products/category/{self.category.id}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["results"][0]["id"], self.product.id)
