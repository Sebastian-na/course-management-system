from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from .models import User, Course, Assignment, Submission, Enrollment
from .validators import date_greater_than_now, period_validator


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True, validators=[
                                   UniqueValidator(queryset=User.objects.all())])
    user_type = serializers.CharField(required=True)
    password = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name',
                  'email', 'user_type', 'password')

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    def validate(self, attrs):
        return super().validate(attrs)


class CourseSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True)
    group = serializers.IntegerField(required=True)
    professor = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = ('id', 'name', 'group', 'professor')

    def get_professor(self, obj):
        return UserSerializer(obj.professor.user).data

    def create(self, validated_data):
        return Course.objects.create(**validated_data, professor=self.context['professor'])


class AssignmentSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=True)
    due_date = serializers.DateTimeField(required=True, input_formats=[
                                         '%Y-%m-%d %H:%M'], validators=[date_greater_than_now])

    class Meta:
        model = Assignment
        fields = ('id', 'name', 'description', 'due_date', 'course')

    def get_course(self, obj):
        return CourseSerializer(obj.course).data

    def create(self, validated_data):
        return Assignment.objects.create(**validated_data, course=self.context['course'])

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get(
            'description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.save()
        return instance


class SubmissionSerializer(serializers.ModelSerializer):
    assignment = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()

    class Meta:
        model = Submission
        fields = ('id', 'assignment', 'student', 'created_at',
                  'grade', 'grade_comment', 'status')

    def get_assignment(self, obj):
        return AssignmentSerializer(obj.assignment).data

    def create(self, validated_data):
        return Submission.objects.create(**validated_data, student=self.context['student'], assignment=self.context['assignment'])

    def update(self, instance, validated_data):
        if 'grade' in validated_data:
            instance.status = Submission.GRADED
        instance.grade = validated_data.get('grade', instance.grade)
        instance.grade_comment = validated_data.get(
            'grade_comment', instance.grade_comment)
        instance.save()
        return instance

    def get_student(self, obj):
        return UserSerializer(obj.student.user).data


class EnrollmentSerializer(serializers.ModelSerializer):
    course = serializers.SerializerMethodField()
    student = serializers.SerializerMethodField()
    period = serializers.IntegerField(
        required=True, validators=[period_validator])

    class Meta:
        model = Enrollment
        fields = ('id', 'student', 'course', 'period')

    def get_course(self, obj):
        return CourseSerializer(obj.course).data

    def get_student(self, obj):
        return UserSerializer(obj.student.user).data

    def create(self, validated_data):
        return Enrollment.objects.create(**validated_data, student=self.context['student'], course=self.context['course'])
