from datetime import date

from django.shortcuts import render
from django.db.models import Count
from django.db import IntegrityError
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


from .models import Restaurant, Employee, Menu, Vote
from .serializers import RestaurantSerializer, EmployeeSerializer,\
    MenuSerializer, VoteSerializer


class CustomBaseModelViewSet(viewsets.ModelViewSet):
    http_method_names = ["post", "get", "put", "patch", "delete"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def create(self, *args, **kwargs):
        try:
            return super(CustomBaseModelViewSet, self).create(*args, **kwargs)
        except IntegrityError as ex:
            return Response(
                data={"detail": "Item cannot be created because: %s" %
                      str(ex)},
                status=status.HTTP_400_BAD_REQUEST)


class RestaurantViewSet(CustomBaseModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Restaurant model.
    """
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class EmployeeViewSet(CustomBaseModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Employee model.
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


class MenuViewSet(CustomBaseModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for Menu model.
    """
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @ action(detail=False, methods=['get'])
    def current_day(self, request):
        menu_items = Menu.objects.filter(created__date=date.today())

        page = self.paginate_queryset(menu_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(menu_items, many=True)
        return Response(serializer.data)

    # preference_param = openapi.Parameter(
    #     'preference_score', openapi.IN_BODY,
    #     description="A integer value representing preference score. Valid values are 1, 2 and 3", type=openapi.TYPE_INTEGER)

    # @swagger_auto_schema(method='post',
    #                      # responses={200: UserSerializer(many=True)},
    #                      manual_parameters=[preference_param]
    #                      )
    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticatedOrReadOnly,])
    def vote(self, request, pk=None):
        menu = self.get_object()
        if menu.created.date() != date.today():
            return Response(
                data={"detail": "Specified menu belongs to past date %s "
                      "and cannot be voted for today" %
                      menu.created.date()},
                status=status.HTTP_400_BAD_REQUEST)
        if request.version and request.version == "2.0":
            # Latest version
            preference_score = request.data.get(
                "preference_score", Vote.Preference.FIRST)
        else:
            # For old version, we assume a preference score of 1 since
            # the user can select only one and thats the topmost then
            preference_score = Vote.Preference.FIRST

        employee = Employee.objects.filter(user=request.user)[0]

        try:
            vote = Vote(employee=employee, menu=menu,
                        preference_score=preference_score,
                        created_by=request.user)
            vote.save()
        except IntegrityError:
            return Response(
                data={"detail": "Employee %s has already voted for preference score value of %d" %
                      (employee.user.username, preference_score)},
                status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Menu is voted successfully"})


class VoteViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read only viewset for Vote model
    """
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer


@ permission_classes([AllowAny,])
class ResultsView(APIView):
    """
    This view returns the top three restaurant's menu that are
    voted by the employees for today's lunch
    """

    def get(self, request):
        top_menu = Menu.objects.annotate(
            num_votes=Count("vote")).order_by("-num_votes")[:3]

        return Response({
            "first": {
                "restaurant_name": top_menu[0].restaurant.name,
                "menu": top_menu[0].id
            },
            "second": {
                "restaurant_name": top_menu[1].restaurant.name,
                "menu": top_menu[1].id
            },
            "third": {
                "restaurant_name": top_menu[2].restaurant.name,
                "menu": top_menu[2].id
            }
        })
