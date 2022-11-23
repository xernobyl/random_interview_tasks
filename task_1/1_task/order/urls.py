from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import order_list

urlpatterns = [
    path('', order_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)
