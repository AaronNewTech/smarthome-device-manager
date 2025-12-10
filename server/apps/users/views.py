from rest_framework import viewsets
from rest_framework.permissions import AllowAny

from server.apps.users.models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
