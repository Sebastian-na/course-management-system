from rest_framework import permissions
from .models import User, Course

class isProfessor(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type == User.PROFESSOR:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True
        
class isProfessorAndOwnsCourse(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type == User.PROFESSOR:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if Course.objects.get(id=request.data["course_id"]).professor.user == request.user:
            return True
        return False