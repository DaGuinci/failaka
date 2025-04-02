from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class SitePermission(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return True
        else:
            return view.action in ['retrieve', 'update', 'partial_update', 'destroy']

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        elif request.user.is_authenticated and request.user.role == 'admin':
            return True
        elif request.user.is_authenticated and request.user == obj.author:
            return True
        return False