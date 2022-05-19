from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager


# Custom User Manager for Custom User Model with email as identifier
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, user_type, **extra_fields):
        if not email:
            raise ValueError(('The Email must be set'))
        if user_type not in [User.PROFESSOR, User.STUDENT, User.ADMIN]:
            raise ValueError(('Invalid user_type'))
        email = self.normalize_email(email)
        user = self.model(email=email, user_type=user_type, **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', User.ADMIN)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)

# Custom User Model for further customizations


class User(AbstractUser):
    username = None
    PROFESSOR = 'Professor'
    STUDENT = 'Student'
    ADMIN = 'Admin'
    USER_TYPE_CHOICES = [(PROFESSOR, 'Professor'),
                         (STUDENT, 'Student'), (ADMIN, 'Admin')]
    user_type = models.CharField(
        choices=USER_TYPE_CHOICES, max_length=20, default=STUDENT)
    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email


class Professor(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.email})"


class Student(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} ({self.user.email})"


class Course(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    group = models.IntegerField()
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, )

    def __str__(self):
        return f"{self.name} - ({self.group})"


class Enrollment(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, )
    # period has the following format: YYYYSemester, example: 20192 (2019 second semester)
    period = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course', 'period'], name='unique_enrollment')
        ]

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - {self.course.name} - ({self.course.group})"


class Assignment(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, default="Assignment")
    description = models.TextField(default="")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, )
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'course'], name='unique_assignment_name_course'),
            models.CheckConstraint(check=models.Q(due_date__gt=models.F(
                'created_at')), name='due_date_gt_created_at')
        ]

    def __str__(self):
        return f"{self.name} - ({self.course.name})"


class Submission(models.Model):
    SENT = 'Sent'
    GRADED = 'Graded'
    STATUS_CHOICES = [
        (SENT, 'Sent'),
        (GRADED, 'Graded'),
    ]
    id = models.AutoField(primary_key=True, editable=False)
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, )
    student = models.ForeignKey(Student, on_delete=models.CASCADE, )
    grade = models.IntegerField(null=True)
    grade_comment = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(choices=STATUS_CHOICES,
                              max_length=20, default=SENT)

    def __str__(self):
        return f"{self.student.user.first_name} {self.student.user.last_name} - {self.assignment.name} - ({self.assignment.course.name})"


class File(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    submission = models.ForeignKey(
        Submission, on_delete=models.CASCADE, null=True)
    assignment = models.ForeignKey(
        Assignment, on_delete=models.CASCADE, null=True, )
    file = models.FileField(null=False, upload_to="media/")

    def __str__(self):
        return f"{self.file.name}"
