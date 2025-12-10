from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import DeviceCategoryViewSet

router = DefaultRouter()
router.register(r"device_categories", DeviceCategoryViewSet, basename="device_category")

urlpatterns = [
    path('', include(router.urls)),
]
