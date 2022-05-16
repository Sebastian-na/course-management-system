from django.contrib import admin
from .models import User, Professor, Student

admin.site.register(User)
admin.site.register(Professor)
admin.site.register(Student)