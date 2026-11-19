from django.contrib.auth import get_user_model

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiExample,
)

from user.serializers import RegisterSerializer, UserSerializer

AUTH_HEADER_PARAMS = [
    OpenApiParameter(
        name="Authorize",
        description="JWT token for authentication",
        required=True,
        location=OpenApiParameter.HEADER,
        examples=[
            OpenApiExample(
                "Bearer Token",
                value="Bearer <your_jwt_token>",
            )
        ],
    )
]

User = get_user_model()


class RegisterAPIView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Method for creating a new user"""
        return self.create(request, *args, **kwargs)


@extend_schema_view(
    get=extend_schema(parameters=AUTH_HEADER_PARAMS),
    put=extend_schema(parameters=AUTH_HEADER_PARAMS),
    patch=extend_schema(parameters=AUTH_HEADER_PARAMS),
)
class UserAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def get(self, request, *args, **kwargs):
        """Get information about the currently authenticated user"""
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Update information about the currently authenticated user"""
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        """Partially update information about the currently authenticated user"""
        return self.partial_update(request, *args, **kwargs)
