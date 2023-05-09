from datetime import date

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Restaurant, Employee, Menu, Vote
from .serializers import RestaurantSerializer, EmployeeSerializer,\
    MenuSerializer, VoteSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Restaurant model.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class EmployeeViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Employee model.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class MenuViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Menu model.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    http_method_names = ['get', 'post', 'put']

    @action(detail=False, methods=['get'])
    def current_day(self, request):
        menu_items = Menu.objects.filter(created__date=date.today())

        page = self.paginate_queryset(menu_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(menu_items, many=True)
        return Response(serializer.data)


class VoteViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Restaurant model.
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
