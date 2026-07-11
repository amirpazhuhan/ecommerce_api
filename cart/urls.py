from django.urls import path

from .views import ViewCart, DeleteItemCart, AddItemCart

urlpatterns=[
    path('items/', AddItemCart.as_view(), name='add-item'),
    path('', ViewCart.as_view(), name="view-cart"),
    path('items/delete/', DeleteItemCart.as_view(), name="delete-item"),
]
