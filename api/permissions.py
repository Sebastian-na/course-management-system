from rest_framework import permissions
from .models import User, Course, Submission, Enrollment, Student

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

class isStudent(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type == User.STUDENT:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        return True

class isStudentAndEnrolled(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.user_type == User.STUDENT:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        student = Student.objects.get(user=request.user)
        course = Course.objects.get(id=request.data["course_id"])
        if Enrollment.objects.filter(student=student, course=course).exists():
            return True
        return False

