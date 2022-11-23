from django.contrib.auth.models import User
from django.db import models
from ..product.models import Product


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, null=False, related_name="orders"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, null=False, related_name="orders"
    )
    quantity = models.PositiveBigIntegerField()
    total_cost = models.PositiveIntegerField()
