from rest_framework.viewsets import ModelViewSet
from entities.models import Comment
from entities.serializers import CommentSerializer
from entities.permissions import ResourcePermission

# Create your views here.
class CommentViewset(ModelViewSet):
    permission_classes = [ResourcePermission]
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        # Attribue l'auteur à partir de l'utilisateur authentifié
        serializer.save(author=self.request.user)