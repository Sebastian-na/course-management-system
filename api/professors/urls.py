
from django.urls import path
from . import views
urlpatterns = [
    path('course/', views.create_course, name='create_course'),
    path("assignment/", views.create_assignment, name="create_assignment"),
    path("assignment/<int:id>/",
         views.update_assignment, name="update_assignment"),
    path("submission/<int:id>/",
         views.update_submission, name="update_submission"),
    path("submissions/<int:assignment_id>/", views.get_submissions_for_assignment,
         name="get_submissions_for_assignment"),
    path("coursestudents/", views.get_students_enrolled_in_course,
         name="get_students_enroll_in_course"),
]