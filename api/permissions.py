from rest_framework import permissions

class IsSelf(permissions.BasePermission):
    """
    Object-level permission to only allow the user to update themselves.
    Used for confirming that the user sending the request is same as the user object that is going to be updated.
    """    
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False
        return obj == request.user
    
class IsSelfOrAdmin(IsSelf):
    """
    Permission is allowed if the user that is requesting is either the owner or an admin.
    """

    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_authenticated and request.user.is_staff:
            return True
        return super().has_object_permission(request, view, obj)
    
class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Object-level permission to only allow the owners of an object to work on it.
    """

    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        
        if hasattr(obj, 'user'):
            return obj.user.username == request.user.username or request.user.is_staff
        return obj.author.username == request.user.username or request.user.is_staff