from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet, EmployeeViewSet, \
    MenuViewSet, VoteViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'restaurant', RestaurantViewSet, basename="restaurant")
router.register(r'employee', EmployeeViewSet, basename="employee")
router.register(r'menu', MenuViewSet, basename="menu")
router.register(r'vote', VoteViewSet, basename="vote")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
