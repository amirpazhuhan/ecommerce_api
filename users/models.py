from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    # Email is the customer's durable contact identifier and must be unique.
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.username
