from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework import permissions
from .serializers import AddToCartSerializer, CartSerializer, DeleteItemSerializer
from rest_framework.response import Response
from .models import Cart, Item
from products.models import Product
# Create your views here.

class AddItemCart(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        product = get_object_or_404(Product, pk=serializer.validated_data['product_id'])
        quantity = serializer.validated_data['quantity']

        # Validate before writing so a rejected request never leaves a cart row.
        item = Item.objects.filter(cart=cart, product=product).first()
        if item:
            quantity += item.quantity
        if quantity > product.stock:
            return Response({"detail": "Insufficient stock."}, status=400)
        if item:
            item.quantity = quantity
            item.save(update_fields=["quantity"])
        else:
            Item.objects.create(cart=cart, product=product, quantity=quantity)

        return Response(CartSerializer(cart).data, status=200)
    



class DeleteItemCart(APIView):
    """
    Deletes an Item from user's cart.
    """
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        serializer = DeleteItemSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
            
        user = request.user
        product_id = serializer.validated_data["product_id"]
        cart = get_object_or_404(Cart, user=user)
        cart_item = get_object_or_404(cart.items, product_id=product_id)
        cart_item.delete()
        return Response(status=204)
    

class ViewCart(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):

        cart, _ = Cart.objects.get_or_create(user=request.user)
        return Response(CartSerializer(cart).data, status=200)
