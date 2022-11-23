import re

from rest_framework import serializers

from ..serializers import PriceField
from .models import Product


class PriceField(serializers.Field):
    """
    Money, in cents...
    """
    def to_representation(self, value: int):
        return f"€{value/100:.2f}"

    def to_internal_value(self, data: str):
        r = re.findall(r"^€(?:(?:([0-9]*)[.])?([0-9]+))$", data)[0]
        if len(r) == 2:
            return int(r[1]) * 100 if r[0] == '' else int(r[0]) * 100 + int(r[1])
        else:
            raise Exception("Wrong format for price.")


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'quantity']

    price = PriceField()
