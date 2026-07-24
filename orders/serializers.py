from rest_framework import serializers

from products.serializers import ProductSerializer

from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serialize a purchased item within an order.

    Includes a nested product representation together with snapshot
    fields that preserve the product name and purchase price at the
    time the order was placed.
    """

    product = ProductSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "product",
            "product_name",
            "quantity",
            "price_at_purchase",
        )


class OrderSerializer(serializers.ModelSerializer):
    """
    Serialize an order together with all purchased items.

    Related order items are exposed through the reverse relationship
    defined by the `orderitems` related name.
    """

    items = OrderItemSerializer(
        many=True,
        read_only=True,
        source="orderitems",
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "status",
            "items",
            "total_price",
            "created_at",
        )
