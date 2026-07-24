from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Custom user model for the e-commerce application.

    Extends Django's built-in AbstractUser by adding customer-specific
    contact and shipping information.
    """

    # Email serves as the customer's primary contact address and must
    # remain unique across all accounts.
    email = models.EmailField(unique=True)

    phone_number = models.CharField(
        max_length=20,
        null=True,
        blank=True,
    )

    address = models.TextField(
        null=True,
        blank=True,
    )

    def __str__(self):
        """
        Return the username for human-readable representations.
        """
        return self.username
