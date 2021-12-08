from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user_id

class IsAuthenticatedForUnsafeMethods():
    """
    Django Rest Framework does not provide permissions on create methods, so adding authentication for unsafe methods
        and ability to view objects who don't have a user
    """

    def has_permission(self, request, view):
        if request.method not in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        
        return True

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user or obj.user is None
        
