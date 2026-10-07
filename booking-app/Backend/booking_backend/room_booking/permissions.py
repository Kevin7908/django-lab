from rest_framework import permissions

# This custom permission allows ANYONE to view the data, but only the 
# creator/owner of the object can edit or delete it.
class IsOwnerOrReadOnly(permissions.BasePermission):

    # 'has_object_permission' runs when a user tries to access a SPECIFIC item (like /posts/1/).
    def has_object_permission(self, request, view, obj):
        # 1. 'SAFE_METHODS' are HTTP requests that don't change data (GET, HEAD, OPTIONS).
        # If the user is just trying to read/view the data, allow it (return True).
        if request.method in permissions.SAFE_METHODS:
            return True

        # 2. If it is NOT a safe method (meaning they want to PUT, PATCH, or DELETE),
        # only allow it if the user making the request is the owner of the object.
        return obj.user == request.user 


# This custom permission allows ANYONE to view the data, but only 
# Admins (superusers) can create, edit, or delete items.
class IsAdminOrReadOnly(permissions.BasePermission):

    # 'has_permission' runs first. It checks if the user has access to the 
    # ENTIRE view or list (like /rooms/). It intercepts POST requests (creation).
    def has_permission(self, request, view):
        # 1. Allow anyone to view the list (GET).
        if request.method in permissions.SAFE_METHODS:
            return True

        # 2. If they are trying to create a new item (POST), they must be an admin.
        return request.user.is_superuser

    # 'has_object_permission' runs second, ONLY if they access a specific item.
    # It intercepts PUT, PATCH, and DELETE requests for individual objects.
    def has_object_permission(self, request, view, obj):
        # 1. Allow anyone to view the specific item (GET).
        if request.method in permissions.SAFE_METHODS:
            return True

        # 2. If they are trying to edit or delete the item, they must be an admin.
        return request.user.is_superuser