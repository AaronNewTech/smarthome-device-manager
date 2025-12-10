"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

baseurl = 'api/v1/'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Include the devices app URLs. Use the full package path so imports resolve
    # correctly when running manage.py from the project root.
    path(f'{baseurl}', include('server.apps.devices.urls')),
    path(f'{baseurl}', include('server.apps.rooms.urls')),
    path(f'{baseurl}', include('server.apps.users.urls')),
    path(f'{baseurl}', include('server.apps.device_logs.urls')),
    path(f'{baseurl}', include('server.apps.device_categories.urls')),
]
