from rest_framework.permissions import BasePermission

class HasOwner(BasePermission):
    def has_permission(self, request, view):
        return request.owner

class IsIndividualSeller(BasePermission):
    def has_permission(self, request, view):
        return request.user_type == "INDIVIDUAL-SELLER"
