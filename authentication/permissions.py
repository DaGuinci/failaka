from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'admin')
        # anyone can create users
        if view.action == 'create':
            if request.data.get('role') and request.data.get('role') != 'visitor':
                raise PermissionDenied("You only have permission to create a visitor.")
            return True
        else:
            return view.action in ['retrieve', 'update', 'partial_update', 'destroy']

    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated and request.user.is_superuser:
            return True
        elif request.user.is_authenticated and request.user.role == 'admin':
            return True
        elif request.user == obj:
            # dont allow role change
            if request.data.get('role') and request.data.get('role') != obj.role:
                raise PermissionDenied("You do not have permission to change the role.")
            return True

        return False