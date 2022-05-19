from django.urls import path
from . import views

urlpatterns = [
    path("enroll/", views.enroll_student, name="enroll_student"),
    path("submission/", views.create_submission, name="create_submission"),
    path("course/", views.get_students_enrolled_in_course,
         name="get_students_enroll_in_course"),
]