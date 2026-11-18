from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from user.serializers import RegisterSerializer


User = get_user_model()


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
