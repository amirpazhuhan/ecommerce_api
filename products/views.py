from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product

# Create your views here.

class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
    
class ProductDetails(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
