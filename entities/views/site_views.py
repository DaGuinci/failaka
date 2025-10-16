from rest_framework.viewsets import ModelViewSet
from entities.models import Site
from entities.serializers import SiteSerializer
from entities.permissions import ResourcePermission
from rest_framework.response import Response

# Create your views here.
class SiteViewset(ModelViewSet):
    permission_classes = [ResourcePermission]
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        # Assign author from authenticated user
        serializer.save(author=self.request.user)