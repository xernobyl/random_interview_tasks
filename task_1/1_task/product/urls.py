from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import product_list

urlpatterns = [
    path('', product_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)
