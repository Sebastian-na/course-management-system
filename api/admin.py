from django.contrib import admin
from .models import *

admin.site.register(User)
admin.site.register(Professor)
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Assignment)
admin.site.register(Submission)
admin.site.register(Enrollment)
admin.site.register(File)

