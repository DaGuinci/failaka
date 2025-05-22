from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from django.contrib.auth.models import Group


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and (
                request.user.is_superuser or request.user.groups.filter(name='admins').exists()
            )
        # anyone can create users
        if view.action == 'create':
            if request.data.get('group') and request.data.get('group') != 'visitors':
                raise PermissionDenied("You only have permission to create a visitor.")
            return True
        else:
            return view.action in ['retrieve', 'update', 'partial_update', 'destroy']

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        elif request.user.is_authenticated and request.user.groups.filter(name='admins').exists():
            return True
        elif request.user == obj:
            # don't allow group change
            if request.data.get('group') and not request.user.groups.filter(name=request.data.get('group')).exists():
                raise PermissionDenied("You do not have permission to change the group.")
            return True

        return False