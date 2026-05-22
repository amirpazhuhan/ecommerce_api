from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework import serializers
from .serializers import AddToCartSerializer, CartSerializer
from rest_framework.response import Response
from .models import Cart, Item
# Create your views here.

class AddItemCart(APIView):
    def post(self, request):
        
        serializer = AddToCartSerializer(data=request.data)
        if serializer.is_valid():
            cart, _ = Cart.objects.get_or_create(user=request.user)
            product_id = serializer.validated_data['product_id']
            quantity = serializer.validated_data['quantity']
        else:
            return Response(serializer.errors , status=400)

        item = Item.objects.filter(cart=cart, item_id = product_id).first()
        

        if item:
            item.quantity += quantity
            item.save()     
        else:
            Item.objects.create(cart=cart, item_id= product_id, quantity=quantity)


        return Response(CartSerializer(cart).data, status=201)