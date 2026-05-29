from django.shortcuts import render

from rest_framework.views import APIView,Response
from rest_framework.exceptions import ValidationError
from django.db import transaction
from .models import Order, OrderItem
from cart.models import Cart

# Create your views here.

class CreateOrder(APIView):

    def post(self, request):


        try:
            with transaction.atomic():
                cart = Cart.objects.get(user=request.user)
                cart_items = cart.items.select_for_update().all()
                
                if not cart_items.exists():
                    return Response({"error": "Cart is empty"}, status=400)
                
                order = Order.objects.create(user= request.user, total_price=0)

                total=0

                for item in cart_items:
                    price = item.item.price

                    if item.item.inventory < item.quantity:
                        raise ValidationError(f"Not enough stock for {item.item.name}")
                    
                    item.item.inventory -= item.quantity
                    item.item.save()

                    order_item = OrderItem.objects.create(
                        order=order,
                        price_at_purchase=price,
                        product=item.item,
                        quantity= item.quantity,
                    )
                    total += price * item.quantity

                order.total_price= total
                order.save()
                cart.items.all().delete()
        except Exception as e:
            return Response({"error": str(e)}, status=400)
