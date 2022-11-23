from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Order
from ..product.models import Product
from .serializers import OrderSerializer


@api_view(['GET', 'POST'])
def order_list(request: Request):
    # create an order
    if request.method == 'POST':
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')

        product = Product.objects.filter(id=product_id)
        # check if product is valid
        if len(product) == 0:
            return Response({"code": 400, "message": "Product doesn't exist"})
        product = product[0]

        # ckeck if product is available
        if product.quantity - quantity < 0:
            return Response({"code": 400, "message": "Not enough quantity"})

        order = Order.objects.create(user=request.user, product=product, quantity=quantity, total_cost=product.price * quantity)
        product.quantity -= quantity
        product.save()

        return Response(OrderSerializer(order).data)

    # list orders
    else:
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
