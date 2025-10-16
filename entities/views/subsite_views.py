from rest_framework.viewsets import ModelViewSet
from entities.models import Subsite
from entities.serializers import SubsiteSerializer
from entities.permissions import ResourcePermission

# Create your views here.
class SubsiteViewset(ModelViewSet):
    permission_classes = [ResourcePermission]
    queryset = Subsite.objects.all()
    serializer_class = SubsiteSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        # Assign author from authenticated user
        serializer.save(author=self.request.user)