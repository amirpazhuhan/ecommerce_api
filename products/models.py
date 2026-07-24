from django.db import models


class Category(models.Model):
    """
    Represents a product category.

    Categories are used to organize products and enable
    category-based browsing and filtering.
    """

    name = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(
        max_length=50,
        unique=True,
        blank=False,
    )

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        """
        Return the category name for human-readable representations.
        """
        return self.name


class Product(models.Model):
    """
    Represents a product available for purchase.

    Each product belongs to a single category and maintains
    inventory information used during the checkout process.
    """

    name = models.CharField(max_length=200)
    description = models.TextField()

    slug = models.SlugField(
        unique=True,
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
    )

    # Products cannot exist without a category. Using PROTECT prevents
    # accidental deletion of categories that still contain products.
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    stock = models.PositiveIntegerField()

    image = models.ImageField(
        upload_to="products/",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """
        Return the product name for the Django admin and shell.
        """
        return self.name
