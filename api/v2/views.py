from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions

from .models import Restaurant
from .serializers import RestaurantSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Restaurant model.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
