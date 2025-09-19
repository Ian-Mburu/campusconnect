from rest_framework import permissions #type: ignore

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a profile to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # SAFE methods like GET, HEAD, OPTIONS are always allowed
        if request.method in permissions.SAFE_METHODS:
            return True

        # Compare against obj.user instead of obj.owner
        return obj.user == request.user
