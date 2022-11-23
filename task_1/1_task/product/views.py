from django.conf import settings
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Product
from .serializers import ProductSerializer


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def product_list(request: Request):
    products = Product.objects.all()

    paginator = PageNumberPagination()
    paginator.page_size = settings.DEFAULT_PAGE_SIZE
    products = paginator.paginate_queryset(products, request)
    serializer = ProductSerializer(products, many=True)

    return Response(serializer.data)
