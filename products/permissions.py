from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner
        return obj.user == request.user

class IsProductOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow product owners or admins to edit products.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner or admin
        return obj.created_by == request.user or request.user.is_staff
    
class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow admin users to create, update, or delete.
    Read-only access for everyone else.
    """
    def has_permission(self, request, view):
        # Allow GET, HEAD, OPTIONS requests for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Only allow admin users for POST, PUT, PATCH, DELETE
        return request.user and request.user.is_staff

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    Custom permission to only allow owners or admins to edit objects.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request
        if request.method in permissions.SAFE_METHODS:
            return True
        
        # Write permissions are only allowed to the owner or admin
        return obj.created_by == request.user or request.user.is_staff