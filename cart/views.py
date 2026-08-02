from django.shortcuts import get_object_or_404

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
)

from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import UpdateAPIView

from products.models import Product
from .models import Cart, Item
from .serializers import (
    AddToCartSerializer,
    CartSerializer,
    ItemSerializer,
)


class AddItemCart(APIView):
    """
    Add a product to the authenticated user's shopping cart.

    If the product already exists in the cart, its quantity is increased
    instead of creating a duplicate cart item.

    The requested quantity is validated against the product's current stock
    before any database modifications are made.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Cart"],
        summary="Add an item to the shopping cart",
        description="""
        Adds a product to the authenticated user's shopping cart.

        Behaviour:
        - Creates a cart automatically if one does not exist.
        - Increases the quantity if the product is already present.
        - Rejects requests that exceed the available stock.
        - Returns the updated cart.
        """,
        request=AddToCartSerializer,
        responses={
            200: CartSerializer,
            400: OpenApiResponse(description="Insufficient stock."),
            401: OpenApiResponse(description="Authentication required."),
        },
    )
    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Ensure every authenticated user has exactly one cart.
        cart, _ = Cart.objects.get_or_create(user=request.user)

        product = get_object_or_404(
            Product,
            pk=serializer.validated_data["product_id"],
        )

        quantity = serializer.validated_data["quantity"]

        # Look for an existing cart item so repeated requests update
        # quantity instead of creating duplicate rows.
        item = Item.objects.filter(
            cart=cart,
            product=product,
        ).first()

        if item:
            quantity += item.quantity

        # Validate stock before writing anything to the database.
        if quantity > product.stock:
            return Response(
                {"detail": "Insufficient stock."},
                status=400,
            )

        if item:
            item.quantity = quantity
            item.save(update_fields=["quantity"])
        else:
            Item.objects.create(
                cart=cart,
                product=product,
                quantity=quantity,
            )

        return Response(CartSerializer(cart).data)


class DeleteItemCart(APIView):
    """
    Remove a product from the authenticated user's shopping cart.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Cart"],
        summary="Remove an item from the shopping cart",
        description="""
        Deletes a product from the authenticated user's shopping cart.

        Returns HTTP 204 when the item has been successfully removed.
        """,
        responses={
            204: OpenApiResponse(description="Item deleted."),
            401: OpenApiResponse(description="Authentication required."),
            404: OpenApiResponse(description="Item not found."),
        },
    )
    def delete(self, request, product_id):

        cart = get_object_or_404(
            Cart,
            user=request.user,
        )

        cart_item = get_object_or_404(
            cart.items,
            product_id=product_id,
        )

        cart_item.delete()

        return Response(status=204)


class ViewCart(APIView):
    """
    Retrieve the authenticated user's shopping cart.

    If the user has not created a cart yet, an empty cart is created
    automatically and returned.
    """

    permission_classes = [permissions.IsAuthenticated]

    @extend_schema(
        tags=["Cart"],
        summary="Retrieve the current shopping cart",
        description="""
        Returns the authenticated user's shopping cart, including
        all cart items and calculated totals.

        An empty cart is created automatically for first-time users.
        """,
        responses={
            200: CartSerializer,
            401: OpenApiResponse(description="Authentication required."),
        },
    )
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data)


@extend_schema(
    tags=["Cart"],
    summary="Decrease the quantity of an item in the shopping cart",
    description="""
    Decreases the quantity of a product in the authenticated user's shopping cart.

    - If the item's quantity is greater than 1, it is decreased by one.
    - If the quantity becomes 0, the item is removed from the cart.

    Returns the updated shopping cart.
    """,
    responses={
        200: CartSerializer,
        404: OpenApiResponse(
            description="Cart or product not found in the shopping cart."
        ),
    },
)
class DecreaseCartItem(APIView):
    """
    Decrease the quantity of a product in the authenticated user's cart.
    Removes the item if its quantity becomes zero.
    """

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, product_id):
        cart = get_object_or_404(Cart, user=request.user)
        cart_item = get_object_or_404(cart.items, product_id=product_id)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

        return Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
