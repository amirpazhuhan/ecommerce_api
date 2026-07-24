from django.conf import settings
from django.db import models

from products.models import Product


class Order(models.Model):
    """
    Represents a customer's completed purchase.

    An order is created during checkout and contains one or more
    OrderItem records that preserve the purchased products and
    their prices at the time of purchase.
    """

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        SHIPPED = "shipped", "Shipped"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    # Final amount charged for the order.
    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        """
        Return a concise identifier for the order.
        """
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    """
    Represents a single purchased product within an order.

    Snapshot fields such as product_name and price_at_purchase
    preserve the purchase history even if the original product
    is later modified.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="orderitems",
    )

    # Preserve what the customer purchased even if the product's
    # name changes in the future.
    product_name = models.CharField(max_length=200)

    # Preserve the historical purchase price independently of the
    # product's current price.
    price_at_purchase = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    # Prevent deletion of products that are referenced by completed
    # orders, preserving order history and referential integrity.
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
    )

    quantity = models.PositiveIntegerField()

    def __str__(self):
        """
        Return a readable representation of the purchased item.
        """
        return f"{self.quantity} × {self.product_name}"
