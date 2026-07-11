from django.urls import path
from .views import CreateOrder, OrderList

urlpatterns = [
    path('', OrderList.as_view(), name='order-list'),
    path('checkout/', CreateOrder.as_view(), name='create-order'),
]
