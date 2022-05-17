from rest_framework import serializers
from .models import User, Course, Assignment, Submission, Enrollment

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

class SubmissionSerializer(serializers.ModelSerializer):
    assignment = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    class Meta:
        model = Submission
        fields = ('assignment', 'student', 'created_at', 'grade', 'grade_comment', 'status')

    def get_assignment(self, obj):
        return AssignmentSerializer(obj.assignment).data
    
    def get_student(self, obj):
        return UserSerializer(obj.student.user).data

class EnrollmentSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    class Meta:
        model = Enrollment
        fields = ('student', 'course', 'period')

    def get_course(self, obj):
        return CourseSerializer(obj.course).data

    def get_student(self, obj):
        return UserSerializer(obj.student.user).data

    
    
