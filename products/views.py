from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ProductSerializer, CategorySerializer
from .models import Product, Category

# Create your views here.


class ProductListView(APIView):
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class CategoryListView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


class CategoryProductsView(APIView):
    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        products = category.products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)
