from django.urls import include
from django.urls import path
from rest_framework import routers

from api.views import UserViewSet

router = routers.DefaultRouter()
router.register(r"users", UserViewSet, basename="users")

# Define routes
urlpatterns = [
    path('', include(router.urls)),
]
