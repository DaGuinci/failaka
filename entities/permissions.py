from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class ResourcePermission(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        elif view.action == 'create':
            return (request.user.is_authenticated and request.user.role in ['admin', 'validator'])
        elif view.action == 'list':
            return True
        else:
            return view.action in ['retrieve', 'update', 'partial_update', 'destroy']

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        elif request.user.is_authenticated and request.user.is_superuser:
            return True
        elif request.user.is_authenticated and request.user.role == 'admin':
            return True
        elif request.user.is_authenticated and request.user == obj.author:
            return True
        return False