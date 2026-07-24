from django.db import transaction
from django.shortcuts import get_object_or_404

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)

from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.models import Cart
from products.models import Product

from .models import Order, OrderItem
from .serializers import OrderSerializer


@extend_schema(
    tags=["Orders"],
    summary="Create an order",
    description="""
    Create an order from the authenticated user's shopping cart.

    Checkout workflow:

    - Requires the user to provide a phone number and shipping address.
    - Locks the cart and all purchased products inside a database transaction.
    - Verifies that sufficient stock exists for every cart item.
    - Creates the order and corresponding order items.
    - Deducts inventory.
    - Calculates the final order total.
    - Clears the shopping cart.

    The entire operation is atomic. If any step fails, all database
    changes are rolled back.
    """,
    request=None,
    responses={
        201: OrderSerializer,
        400: OpenApiResponse(
            description="Cart is empty or product stock is insufficient."
        ),
        401: OpenApiResponse(
            description="Authentication required."
        ),
    },
)
class CreateOrder(APIView):
    """
    Convert the authenticated user's shopping cart into an order.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """
        Complete the checkout process.

        Returns the newly created order on success.
        """

        if not request.user.phone_number or not request.user.address:
            raise ValidationError(
                "Phone number and address are required to place an order."
            )

        # Execute the entire checkout as a single database transaction.
        # Either every step succeeds or all changes are rolled back.
        with transaction.atomic():

            # Lock the cart to prevent concurrent checkout requests
            # from modifying it simultaneously.
            cart = get_object_or_404(
                Cart.objects.select_for_update(),
                user=request.user,
            )

            # Fetch all cart items together with their related products
            # to avoid additional database queries while processing.
            cart_items = list(
                cart.items.select_related("product")
                .all()
            )

            if not cart_items:
                return Response(
                    {"detail": "Cart is empty."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Lock every product being purchased. Locking only the cart
            # would still allow another checkout to reduce the same
            # product's stock concurrently.
            products = {
                product.id: product
                for product in Product.objects.select_for_update().filter(
                    id__in=[item.product_id for item in cart_items]
                )
            }

            # Verify stock before creating any database records.
            for item in cart_items:
                product = products.get(item.product_id)

                if product is None or product.stock < item.quantity:
                    raise ValidationError(
                        f"Not enough stock for {item.product.name}"
                    )

            order = Order.objects.create(
                user=request.user,
                total_price=0,
            )

            total = 0

            for item in cart_items:
                product = products[item.product_id]

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    product_name=product.name,
                    price_at_purchase=product.price,
                    quantity=item.quantity,
                )

                # Reduce available inventory only after successful
                # stock validation for the entire order.
                product.stock -= item.quantity
                product.save(update_fields=["stock"])

                total += product.price * item.quantity

            order.total_price = total
            order.save(update_fields=["total_price"])

            # Remove purchased items from the user's cart after the
            # order has been successfully created.
            cart.items.all().delete()

        return Response(
            OrderSerializer(order).data,
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    tags=["Orders"],
    summary="List user orders",
    description="""
    Retrieve all orders belonging to the authenticated user.

    Related order items and products are prefetched to minimize
    database queries during serialization.
    """,
    responses={
        200: OrderSerializer(many=True),
        401: OpenApiResponse(
            description="Authentication required."
        ),
    },
)
class OrderList(APIView):
    """
    List all orders placed by the authenticated user.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        """
        Return the authenticated user's order history.
        """

        # Prefetch related objects to avoid N+1 queries while
        # serializing order items.
        orders = (
            Order.objects
            .filter(user=request.user)
            .prefetch_related("orderitems__product")
        )

        return Response(
            OrderSerializer(orders, many=True).data
        )
