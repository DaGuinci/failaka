from rest_framework.viewsets import ModelViewSet
from entities.models import Mission
from entities.serializers import MissionSerializer
from entities.permissions import ResourcePermission

# Create your views here.
class MissionViewset(ModelViewSet):
    permission_classes = [ResourcePermission]
    queryset = Mission.objects.all()
    serializer_class = MissionSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        # Assign author from authenticated user
        serializer.save(author=self.request.user)