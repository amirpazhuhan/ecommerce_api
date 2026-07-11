from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import Order, OrderItem
from cart.models import Cart
from products.models import Product
from .serializers import OrderSerializer

# Create your views here.

class CreateOrder(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        with transaction.atomic():
            cart = get_object_or_404(Cart.objects.select_for_update(), user=request.user)
            cart_items = list(cart.items.select_related("product").all())
            if not cart_items:
                return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

            # Lock products too; locking only cart rows can still oversell stock.
            products = {
                product.id: product
                for product in Product.objects.select_for_update().filter(
                    id__in=[item.product_id for item in cart_items]
                )
            }
            for item in cart_items:
                product = products.get(item.product_id)
                if product is None or product.stock < item.quantity:
                    raise ValidationError(f"Not enough stock for {item.product.name}")

            order = Order.objects.create(user=request.user, total_price=0)
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
                product.stock -= item.quantity
                product.save(update_fields=["stock"])
                total += product.price * item.quantity

            order.total_price = total
            order.save(update_fields=["total_price"])
            cart.items.all().delete()
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)


class OrderList(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user).prefetch_related("orderitems__product")
        return Response(OrderSerializer(orders, many=True).data)
