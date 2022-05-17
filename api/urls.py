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
    path('create/course/', views.create_course, name='create_course'),
    path("create/assignment/", views.create_assignment, name="create_assignment"),
    path("update/assignment/<int:id>/", views.update_assignment, name="update_assignment"),
    path("create/submission/", views.create_submission, name="create_submission"),
    path("student/enroll/", views.enroll_student, name="enroll_student"),
]