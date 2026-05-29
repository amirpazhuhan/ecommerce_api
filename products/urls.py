from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name="products-list"),
    path('<int:pk>/', views.ProductDetails.as_view(), name="product-detail"),
]