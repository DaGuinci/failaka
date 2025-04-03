from rest_framework.viewsets import ModelViewSet
from entities.models import Item
from entities.serializers import ItemSerializer
from entities.permissions import ResourcePermission

# Create your views here.
class ItemViewset(ModelViewSet):
    permission_classes = [ResourcePermission]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        # Attribue l'auteur à partir de l'utilisateur authentifié
        serializer.save(author=self.request.user)