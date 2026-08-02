from rest_framework import serializers

from .models import Category, Product


class ProductSerializer(serializers.ModelSerializer):
    """
    Serialize product data for product listings.

    This serializer provides a lightweight representation suitable
    for catalog and search results.
    """

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "category",
        )


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "slug",
            "stock",
            "price",
            "category",
        )


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Serialize detailed information for a single product.

    Extends the list representation by including the product image.
    """

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "description",
            "price",
            "category",
            "image",
        )


class CategorySerializer(serializers.ModelSerializer):
    """
    Serialize product category information.
    """

    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )
