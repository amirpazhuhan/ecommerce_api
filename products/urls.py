from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name="products-list"),
    path('<int:pk>/', views.ProductDetailView.as_view(), name="product-detail"),
    path('categories/', views.CategoryListView.as_view(), name='category-list-view'),
    path('category/<int:pk>/', views.CategoryProductsView.as_view(), name='category-list-products'),
    
]