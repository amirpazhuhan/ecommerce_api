from rest_framework import serializers

from products.models import Product
from products.serializers import ProductSerializer

from .models import Cart, Item


class ItemSerializer(serializers.ModelSerializer):
    """
    Serialize an individual cart item.

    Includes a nested product representation so clients receive
    product details without making additional API requests.
    """

    product = ProductSerializer(read_only=True)

    class Meta:
        model = Item
        fields = (
            "id",
            "product",
            "quantity",
        )


class CartSerializer(serializers.ModelSerializer):
    """
    Serialize a user's shopping cart.

    Returns all cart items together with the dynamically calculated
    total price of the cart.
    """

    total_price = serializers.SerializerMethodField()
    items = ItemSerializer(many=True, read_only=True)

    def get_total_price(self, obj):
        """
        Return the current total value of the shopping cart.

        The value is calculated by the Cart model to ensure the serializer
        always reflects the latest product prices.
        """
        return obj.get_total_price

    class Meta:
        model = Cart
        fields = (
            "id",
            "user",
            "items",
            "total_price",
        )


class AddToCartSerializer(serializers.Serializer):
    """
    Validate input for adding a product to the shopping cart.
    """

    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        """
        Ensure the requested product exists before attempting to
        create or update a cart item.
        """

        # Fail fast with a clear validation error instead of allowing
        # the view to continue with an invalid product ID.
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("This product does not exist.")

        return value
