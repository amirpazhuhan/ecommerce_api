from django.db import models
from django.contrib.auth.models import User
from .models import Product
# Create your models here.

class Cart(models.Model):

    user = models.OneToOneField(User)
    updated_at = models.DateTimeField(auto_now=True)

    @ property
    def get_total_price(self):
        total_price = 0
        for each in self.items.all():
            total_price += each.quantity * each.item.price
    

class Item(models.Model):

    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField() 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')

