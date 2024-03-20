from django.urls import include, path
from rest_framework import routers
from .views import FlightsViewSet

router = routers.DefaultRouter()
router.register(r"flights", FlightsViewSet)

urlpatterns = [path("", include(router.urls))]
