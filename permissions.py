from rest_framework.permissions import BasePermission

class HasOwner(BasePermission):
    def has_permission(self, request, view):
        return request.owner
