from rest_framework.viewsets import ModelViewSet
from entities.models import Item
from entities.serializers import ItemSerializer
from entities.permissions import ResourcePermission
# from rest_framework.response import Response

# Create your views here.
class ItemViewset(ModelViewSet):
    permission_classes = [ResourcePermission]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def perform_create(self, serializer):
        # Assign author from authenticated user
        serializer.save(author=self.request.user)

    # def retrieve(self, request, *args, **kwargs):
    #     print("retrieve")
    #     # Retrieve the site instance
    #     instance = self.get_object()
    #     # Serialize the site data
    #     serializer = self.get_serializer(instance)
    #     data = serializer.data
    #     # Add the "author_name" field based on the site's author
    #     data['author_name'] = instance.author.username if instance.author else None
    #     return Response(data)
    
    # def list(self, request, *args, **kwargs):
    #     print("list")
    #     # Get the queryset with preloaded related data
    #     queryset = self.filter_queryset(self.get_queryset().select_related('author'))
    #     # Serialize the data
    #     serializer = self.get_serializer(queryset, many=True)
    #     data = serializer.data
    #     # Add the "author_name" field to each item in the list
    #     for item, instance in zip(data, queryset):
    #         item['author_name'] = instance.author.username if instance.author else None
    #     return Response(data)