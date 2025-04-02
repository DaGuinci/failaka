from rest_framework.viewsets import ModelViewSet
from entities.models import Site
from entities.serializers import SiteSerializer
from entities.permissions import ResourcePermission

# Create your views here.
class SiteViewset(ModelViewSet):
    permission_classes = [ResourcePermission]
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        # Attribue l'auteur à partir de l'utilisateur authentifié
        serializer.save(author=self.request.user)