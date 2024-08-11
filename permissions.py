from rest_framework.permissions import BasePermission
from user.models import CustomUser


class HasOwner(BasePermission):
    def has_permission(self, request, view):
        return request.owner

class IsIndividualSeller(BasePermission):
    def has_permission(self, request, view):
        return request.owner.user_type == CustomUser.TypeChoices.INDIVIDUAL_SELLER
