from rest_framework.viewsets import ModelViewSet
from entities.models import Notable
from entities.serializers import NotableSerializer
from entities.permissions import ResourcePermission

# Create your views here.
class NotableViewset(ModelViewSet):
    permission_classes = [ResourcePermission]
    queryset = Notable.objects.all()
    serializer_class = NotableSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        # Attribue l'auteur à partir de l'utilisateur authentifié
        serializer.save(author=self.request.user)