from rest_framework import serializers
from .models import User, Course, Assignment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'user_type')

class CourseSerializer(serializers.ModelSerializer):
    professor = serializers.SerializerMethodField()
    class Meta:
        model = Course
        fields = ('name', 'group', 'professor')

    def get_professor(self, obj):
        return UserSerializer(obj.professor.user).data

class AssignmentSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    class Meta:
        model = Assignment
        fields = ('name', 'description', 'due_date', 'course')
    
    def get_course(self, obj):
        return CourseSerializer(obj.course).data
