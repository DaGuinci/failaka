from rest_framework import status
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import Group

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

    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['post'],
        url_path='add-to-group',
    )
    def add_to_group(self, request, pk=None):
        """
        Add a user to a group, replacing any existing groups.
        """
        try:
            user = self.get_object()  # Get the user instance by pk
            group_name = request.data.get('group_name')
            if not group_name:
                return Response({"detail": "Group name is required."}, status=status.HTTP_400_BAD_REQUEST)

            group = Group.objects.get(name=group_name)
            user.groups.set([group])  # Replace existing groups with the new group
            return Response({"detail": f"User {user.username} added to group {group.name}."}, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"detail": "Group not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)