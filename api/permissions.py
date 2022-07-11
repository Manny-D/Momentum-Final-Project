from rest_framework import permissions

class IsChefOrReadOnly(permissions.BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.note_by == request.user:
            return True
        return False

class RecipeIsChefOrReadOnly(permissions.BasePermission):
    message = 'Editing posts is restricted to the author only.'

    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if obj.chef == request.user:
            return True
        return False