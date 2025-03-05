from rest_framework.permissions import BasePermission


# class IsAuthenticated(BasePermission):

#     def has_permission(self, request, view):
#         return bool(request.user and request.user.is_authenticated)


class UserPermission(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list':
            return request.user.is_authenticated and (request.user.is_superuser or request.user.role == 'admin')
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
                return False
            return True

        return False