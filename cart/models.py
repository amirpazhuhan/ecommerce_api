from django.db import models

from django.conf import settings
from products.models import Product

# Create your models here.


class Cart(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_total_price(self):
        total_price = 0
        for each in self.items.select_related("product"):
            total_price += each.quantity * each.product.price
        return total_price


class Item(models.Model):
    # A product can be present in many customers' carts.
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("cart", "product"), name="unique_cart_product")
        ]
