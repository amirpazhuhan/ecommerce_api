from django.conf import settings
from django.db import models

from products.models import Product


class Cart(models.Model):
    """
    Represents a user's shopping cart.

    Each user owns exactly one cart. Cart items are stored separately
    through the Item model.
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
    )
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_total_price(self):
        """
        Calculate the current total value of the shopping cart.

        The total is computed dynamically using the latest product prices
        rather than being stored in the database.
        """
        total_price = 0

        # Fetch each item's related product in the same query to avoid
        # executing an additional query for every cart item (N+1 problem).
        for item in self.items.select_related("product"):
            total_price += item.quantity * item.product.price

        return total_price


class Item(models.Model):
    """
    Represents a single product inside a shopping cart.
    """

    # A product can appear in many different users' carts.
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )

    quantity = models.PositiveIntegerField()

    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
        related_name="items",
    )

    class Meta:
        # Prevent duplicate rows for the same product within a single cart.
        # Quantity updates should modify the existing row instead.
        constraints = [
            models.UniqueConstraint(
                fields=("cart", "product"),
                name="unique_product_per_cart",
            )
        ]
