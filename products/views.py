from django.shortcuts import get_object_or_404

from rest_framework import django_filters as filters
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import (
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
    extend_schema_view,
)

from .models import Category, Product
from .serializers import (
    CategorySerializer,
    ProductDetailSerializer,
    ProductSerializer,
    CreateProductSerializer,
)


class ProductFilter(filters.FilterSet):
    """
    Filter products by category and price range.

    Supported query parameters:
    - category
    - min_price
    - max_price
    """

    min_price = filters.NumberFilter(
        field_name="price",
        lookup_expr="gte",
    )

    max_price = filters.NumberFilter(
        field_name="price",
        lookup_expr="lte",
    )

    class Meta:
        model = Product
        fields = ["category"]


@extend_schema(
    tags=["Products"],
    summary="List products",
    description="""
    Retrieve a paginated list of products.

    Supports filtering by category and price range,
    full-text search, and ordering.
    """,
    parameters=[
        OpenApiParameter(
            "category",
            int,
            description="Filter products by category ID.",
        ),
        OpenApiParameter(
            "min_price",
            float,
            description="Return products with a price greater than or equal to this value.",
        ),
        OpenApiParameter(
            "max_price",
            float,
            description="Return products with a price less than or equal to this value.",
        ),
        OpenApiParameter(
            "search",
            str,
            description="Search by product name or description.",
        ),
        OpenApiParameter(
            "ordering",
            str,
            description="Sort by 'price', '-price', 'name', or '-name'.",
        ),
    ],
    responses={
        200: ProductSerializer(many=True),
    },
)
class ProductListView(ListAPIView):
    """
    List all available products.

    Clients can filter, search, and order the result set
    using query parameters.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        SearchFilter,
        OrderingFilter,
    ]

    filterset_class = ProductFilter
    search_fields = ["name", "description"]
    ordering_fields = ["price", "name"]


class ProductDetailView(APIView):
    """
    Retrieve detailed information about a single product.
    """

    @extend_schema(
        tags=["Products"],
        summary="Retrieve a product",
        description="""
        Returns detailed information for a single product.

        The product is identified by its primary key.
        """,
        responses={
            200: ProductDetailSerializer,
            404: OpenApiResponse(description="Product not found."),
        },
    )
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data)


@extend_schema(
    summary="Create a product",
    description=(
        "Creates a new product. "
        "Only admin (staff) users are allowed to access this endpoint."
    ),
    request=CreateProductSerializer,
    responses={
        201: CreateProductSerializer,
        400: None,
        401: None,
        403: None,
    },
    tags=["Products"],
)
class CreateProductView(CreateAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer
    permission_classes = [IsAdminUser]


from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiResponse,
)
from rest_framework.generics import UpdateAPIView, DestroyAPIView
from rest_framework.permissions import IsAdminUser


@extend_schema_view(
    put=extend_schema(
        tags=["Products"],
        summary="Update a product",
        description="Update all fields of an existing product. Only administrators can perform this action.",
        responses={
            200: CreateProductSerializer,
            400: OpenApiResponse(description="Invalid data."),
            401: OpenApiResponse(description="Authentication required."),
            403: OpenApiResponse(description="Admin privileges required."),
            404: OpenApiResponse(description="Product not found."),
        },
    ),
    patch=extend_schema(
        tags=["Products"],
        summary="Partially update a product",
        description="Update one or more fields of an existing product. Only administrators can perform this action.",
        responses={
            200: CreateProductSerializer,
            400: OpenApiResponse(description="Invalid data."),
            401: OpenApiResponse(description="Authentication required."),
            403: OpenApiResponse(description="Admin privileges required."),
            404: OpenApiResponse(description="Product not found."),
        },
    ),
)
class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer
    permission_classes = [IsAdminUser]


@extend_schema(
    tags=["Products"],
    summary="Delete a product",
    description="Delete an existing product. Only administrators can perform this action.",
    responses={
        204: OpenApiResponse(description="Product deleted successfully."),
        401: OpenApiResponse(description="Authentication required."),
        403: OpenApiResponse(description="Admin privileges required."),
        404: OpenApiResponse(description="Product not found."),
    },
)
class ProductDeleteView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = CreateProductSerializer
    permission_classes = [IsAdminUser]


class CategoryListView(APIView):
    """
    List all product categories.
    """

    @extend_schema(
        tags=["Categories"],
        summary="List categories",
        description="Retrieve every available product category.",
        responses={
            200: CategorySerializer(many=True),
        },
    )
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)


@extend_schema(
    tags=["Categories"],
    summary="List products in a category",
    description="Retrieve all products that belong to the specified category.",
    responses={
        200: ProductSerializer(many=True),
    },
)
class CategoryProductsView(ListAPIView):
    """
    List all products belonging to a specific category.
    """

    serializer_class = ProductSerializer

    def get_queryset(self):
        # Filter products by the category identifier supplied in the URL.
        return Product.objects.filter(
            category=self.kwargs["pk"],
        )
