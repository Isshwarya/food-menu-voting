from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        if "admin" in (group.name.lower() for group in request.user.groups.all()):
            # admin user can edit anyone's object
            return True
        print("Isshwarya %s" % (obj.created_by == request.user.id))
        return obj.created_by == request.user.id
