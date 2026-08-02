from django.urls import path

from .views import ViewCart, DeleteItemCart, AddItemCart, DecreaseCartItem

urlpatterns = [
    path("items/add/", AddItemCart.as_view(), name="add-item"),
    path(
        "items/decrease/<int:product_id>",
        DecreaseCartItem.as_view(),
        name="decrease-item",
    ),
    path("", ViewCart.as_view(), name="view-cart"),
    path("items/delete/<int:product_id>", DeleteItemCart.as_view(), name="delete-item"),
]
