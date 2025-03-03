from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from authentication.models import User
from authentication.serializers import UserSerializer, RegisterSerializer
from authentication.permissions import UserPermission

from drf_spectacular.utils import extend_schema_view, extend_schema


@extend_schema_view(
    list=extend_schema(
        summary="Récupérer tous les profils.",
        description="Autorisation: superuser.",
    ),
    retrieve=extend_schema(
        summary="Récupérer un profil.",
        description="Autorisation: superuser, propriétaire du profil.",
    ),
    partial_update=extend_schema(
        description="Autorisation: superuser, propriétaire du profil.",
    ),
    destroy=extend_schema(
        description="Autorisation: superuser, propriétaire du profil.",
    ),
)

class UserViewset(ModelViewSet):
    permission_classes = [UserPermission]

    http_method_names = ['get', 'patch', 'delete']

    serializer_class = UserSerializer

    # def list(self, request):
    #     queryset = User.objects.all()
    #     serializer = UserSerializer(queryset, many=True)
    #     return Response(serializer.data)

    def get_queryset(self):
        return User.objects.all()


class RegisterViewset(CreateAPIView):

    queryset = User.objects.all()

    serializer_class = RegisterSerializer