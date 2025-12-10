from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DeviceViewSet

router = DefaultRouter()
router.register(r"devices", DeviceViewSet, basename="devices")


urlpatterns = [
    # Use router-driven endpoints for all standard CRUD on devices.
    # POST /api/v1/devices/ (create) and GET /api/v1/devices/ (list) are
    # provided by the registered DeviceViewSet.
    path("", include(router.urls)),
]

