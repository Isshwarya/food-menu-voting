from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RestaurantViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'restaurant', RestaurantViewSet, basename="restaurant")

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
