from django.db import models
from django.core.exceptions import ValidationError

# Define category choices
CATEGORY_CHOICES = [
    ("PC", "Personal Care"),
    ("FA", "Fashion"),
    ("OF", "Organic Food"),
    ("KD", "Kitchen and Decor"),
    ("EL", "Electronics"),
    ("EKB", "Eco-Friendly Kids & Babies"),

]

class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name="Product Name")
    description = models.TextField(verbose_name="Product Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")
    stock = models.PositiveIntegerField(verbose_name="Stock Quantity")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20, default='PC', verbose_name="Category")
    image = models.ImageField(upload_to='products/', blank=True, null=True, verbose_name="Product Image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def clean(self):
        if self.price <= 0:
            raise ValidationError({'price': 'Price must be greater than 0.'})
        if self.stock < 0:
            raise ValidationError({'stock': 'Stock cannot be negative.'})
