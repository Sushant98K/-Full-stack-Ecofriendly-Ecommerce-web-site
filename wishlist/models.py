from django.db import models
from users.models import CustomUser

class Wishlist(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='wishlist')
    product_name = models.CharField(max_length=255)
    product_url = models.URLField()
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.product_name
