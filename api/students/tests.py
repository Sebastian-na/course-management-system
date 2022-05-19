from django.test import TestCase
from rest_framework.test import APIClient
from ..models import Student, Assignment, Enrollment, Submission


class TestViewEnrollStudent(TestCase):
    client2 = APIClient()

    def setUp(self) -> None:
        self.client.post('/api/auth/register/professor/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "professor@gmail.com", 'password': "password"})
        self.client.post('/api/auth/register/student/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "example@gmail.com", 'password': "password"})
        professor_access = self.client.post(
            '/api/auth/token/', {'email': "professor@gmail.com", 'password': "password"}).data.get("access")
        self.client2.credentials(
            HTTP_AUTHORIZATION='Bearer ' + professor_access)
        course = self.client2.post("/api/professors/course/", {
            'name': "Math", 'group': 8})

        student_access = self.client.post(
            '/api/auth/token/', {'email': "example@gmail.com", 'password': 'password'}).data.get("access")
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + student_access)

    def test_enroll_student(self):
        response = self.client2.post(
            "/api/students/enroll/", {"course_id": 1, "period": 20222})
        e = Enrollment.objects.get(student_id=1, course_id=1)
        self.assertEqual(e.period, 20222)
        self.assertEqual(response.status_code, 201)

    def test_raises_error_when_course_id_is_missing(self):
        response = self.client2.post(
            "/api/students/enroll/", {"period": 20222})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_period_is_missing(self):
        response = self.client2.post("/api/students/enroll/", {"course_id": 1})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_course_id_does_not_exist(self):
        response = self.client2.post(
            "/api/students/enroll/", {"course_id": 2, "period": 20222})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_period_format_is_wrong(self):
        response = self.client2.post(
            "/api/students/enroll/", {"course_id": 1, "period": 20223})
        self.assertEqual(response.status_code, 400)


class TestViewCreateSubmission(TestCase):
    client2 = APIClient()

    def setUp(self) -> None:
        self.client.post('/api/auth/register/professor/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "professor@gmail.com", 'password': "password"})
        self.client.post('/api/auth/register/student/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "example@gmail.com", 'password': "password"})
        professor_access = self.client.post(
            '/api/auth/token/', {'email': "professor@gmail.com", 'password': "password"}).data.get("access")
        self.client2.credentials(
            HTTP_AUTHORIZATION='Bearer ' + professor_access)
        course = self.client2.post("/api/professors/course/", {
            'name': "Math", 'group': 8})
        assignment = self.client2.post("/api/professors/assignment/", {
                                       "name": "Assignment 1", "course_id": 1, "due_date": "2023-01-01 00:00", "description": "This is an assignment"})

        student_access = self.client.post(
            '/api/auth/token/', {'email': "example@gmail.com", 'password': 'password'}).data.get("access")
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + student_access)
        self.client2.post("/api/students/enroll/",
                          {"course_id": 1, "period": 20222})

    def test_create_submission(self):

        response = self.client2.post(
            "/api/students/submission/", {"assignment_id": 1, "course_id": 1})
        a = Assignment.objects.get(id=1)
        s = Student.objects.get(id=1)
        su = Submission.objects.filter(assignment=a, student=s)
        self.assertEqual(response.status_code, 201)

    def test_raises_error_when_assignment_id_is_missing(self):
        response = self.client2.post(
            "/api/students/submission/", {"course_id": 1})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_assignment_id_does_not_exist(self):
        response = self.client2.post(
            "/api/students/submission/", {"assignment_id": 2, "course_id": 1})
        self.assertEqual(response.status_code, 400)
