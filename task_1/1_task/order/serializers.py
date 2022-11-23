from rest_framework import serializers

from ..serializers import PriceField
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'product', 'quantity', 'total_cost']

    total_cost = PriceField()
