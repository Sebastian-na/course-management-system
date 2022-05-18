from django.urls import path
from api import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path("register/professor/", views.register_professor,
         name="register_professor"),
    path("register/student/", views.register_student, name="register_student"),
    path('create/course/', views.create_course, name='create_course'),
    path("create/assignment/", views.create_assignment, name="create_assignment"),
    path("update/assignment/<int:id>/",
         views.update_assignment, name="update_assignment"),
    path("enroll/student/", views.enroll_student, name="enroll_student"),
    path("create/submission/", views.create_submission, name="create_submission"),
    path("update/submission/<int:id>/",
         views.update_submission, name="update_submission"),
    path("students/course/", views.get_students_enrolled_in_course,
         name="get_students_enroll_in_course"),
    path("submissions/<int:assignment_id>/", views.get_submissions_for_assignment,
         name="get_submissions_for_assignment"),
]
