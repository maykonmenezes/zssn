from rest_framework import permissions


class SurvivorReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        # Read permissions are allowed to any survivor,
        # so we allow GET, HEAD or OPTIONS requests.
        return request.method in permissions.SAFE_METHODS
           
        # Write permissions are not allowed for survivors.
        #return obj.infected == False