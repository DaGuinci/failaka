from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from entities.models import Site
from entities.serializers import SiteSerializer
from entities.permissions import SitePermission

# Create your views here.
class SiteViewset(ModelViewSet):
    permission_classes = [SitePermission]
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']