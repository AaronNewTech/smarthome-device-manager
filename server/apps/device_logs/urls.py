from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DeviceLogViewSet

router = DefaultRouter()
router.register(r"device_logs", DeviceLogViewSet, basename="device_log")

urlpatterns = [
    path('', include(router.urls)),
]
