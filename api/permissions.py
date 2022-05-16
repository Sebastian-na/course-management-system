from rest_framework import permissions
from .models import User

class isProfessor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type == User.PROFESSOR:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True