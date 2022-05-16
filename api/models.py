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
    USER_TYPE_CHOICES = [(PROFESSOR, 'Professor'), (STUDENT, 'Student'), (ADMIN, 'Admin')]
    user_type = models.CharField(choices=USER_TYPE_CHOICES, max_length=20, default=STUDENT)
    email = models.EmailField(('email address'), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email


# Create your models here.
class Professor(models.Model):
    id = models.AutoField(primary_key=True, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Student(models.Model):
    id = models.AutoField(primary_key=True, editable=False)                        
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.user.first_name + " " + self.user.last_name


