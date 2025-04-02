from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from authentication.models import User
from authentication.serializers import UserSerializer, RegisterSerializer
from authentication.permissions import UserPermission

from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    list=extend_schema(
        summary="Get all users.",
        description="Autorisation: admin, superuser.",
    ),
    create=extend_schema(
        summary="Register a new user.",
        description="Autorisation: anyone.",
    ),
    retrieve=extend_schema(
        summary="Get a user by id.",
        description="Autorisation: admin, superuser, profile owner.",
    ),
    partial_update=extend_schema(
        description="Autorisation: admin, superuser, profile owner.",
    ),
    destroy=extend_schema(
        description="Autorisation: admin, superuser, profile owner.",
    ),
)

class UserViewset(ModelViewSet):
    permission_classes = [UserPermission]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # dont use put method
    http_method_names = ['get', 'post', 'patch', 'delete']

    # @action(
    #         detail=False,
    #         methods=['post'],
    #         serializer_class=RegisterSerializer,
    #         url_path='register',
    #         permission_classes=[AllowAny]
    #     )
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)