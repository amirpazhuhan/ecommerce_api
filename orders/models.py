from django.db import models

from django.conf import settings
from products.models import Product

# Create your models here.

class Order(models.Model):
    choices = [
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('paid', 'Paid')
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=choices, default='pending')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    price_at_purchase = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveBigIntegerField()