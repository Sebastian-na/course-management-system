from django.test import TestCase
from rest_framework.test import APIClient
from ..models import Course, Assignment, Submission


class TestViewCreateCourse(TestCase):
    client2 = APIClient()

    def setUp(self) -> None:
        self.client.post('/api/auth/register/professor/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "professor@gmail.com", 'password': "password"})
        response = self.client.post(
            '/api/auth/token/', {'email': "professor@gmail.com", 'password': "password"})
        self.client2.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data['access'])

    def test_create_course(self):
        response = self.client2.post('/api/professors/course/', {
            'name': "Math", 'group': 8})
        c = Course.objects.get(id=1)
        self.assertEqual(c.name, "Math")
        self.assertEqual(response.status_code, 201)

    def test_raises_error_when_name_is_missing(self):
        response = self.client2.post('/api/professors/course/', {
            'group': 8})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_group_is_missing(self):
        response = self.client2.post('/api/professors/course/', {
            'name': "Math"})
        self.assertEqual(response.status_code, 400)


class TestViewCreateAssignment(TestCase):
    client2 = APIClient()
    course_id: int

    def setUp(self) -> None:
        self.client.post('/api/auth/register/professor/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "professor@gmail.com", 'password': "password"})
        response = self.client.post(
            '/api/auth/token/', {'email': "professor@gmail.com", 'password': "password"})
        self.client2.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        course = self.client2.post("/api/professors/course/", {
            'name': "Math", 'group': 8})

    def test_create_assignment(self):
        response = self.client2.post("/api/professors/assignment/", {
                                     "name": "Assignment 1", "course_id": 1, "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        a = Assignment.objects.get(id=1)
        self.assertEqual(a.name, "Assignment 1")
        self.assertEqual(response.status_code, 201)

    def test_raises_error_when_name_is_missing(self):
        response = self.client2.post("/api/professors/assignment/", {
                                     "course_id": 1, "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_course_id_is_missing(self):
        response = self.client2.post("/api/professors/assignment/", {
                                     "name": "Assignment 1", "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_due_date_is_missing(self):
        response = self.client2.post("/api/professors/assignment/", {
                                     "name": "Assignment 1", "course_id": 1, "description": "This is an assignment"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_description_is_missing(self):
        response = self.client2.post("/api/professors/assignment/", {
                                     "name": "Assignment 1", "course_id": 1, "due_date": "2023-01-01 00:00"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_course_id_does_not_exist(self):
        response = self.client2.post("/api/professors/assignment/", {
                                     "name": "Assignment 1", "course_id": 2, "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_due_date_is_in_the_past(self):
        response = self.client2.post("/api/professors/assignment/", {
                                     "name": "Assignment 1", "course_id": 1, "due_date": "2020-01-01 00:00", "description": "This is an assignment"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_due_date_format_is_wrong(self):
        response = self.client2.post("/api/professors/assignment/", {
                                     "name": "Assignment 1", "course_id": 1, "due_date": "2023/01/01", "description": "This is an assignment"})
        self.assertEqual(response.status_code, 400)


class TestViewUpdateAssignment(TestCase):
    client2 = APIClient()

    def setUp(self) -> None:
        self.client.post('/api/auth/register/professor/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "professor@gmail.com", 'password': "password"})
        response = self.client.post(
            '/api/auth/token/', {'email': "professor@gmail.com", 'password': "password"})
        self.client2.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        course = self.client2.post("/api/professors/course/", {
            'name': "Math", 'group': 8})

    def test_update_assignment(self):
        response = self.client2.post("/api/professors/assignment/", {
                                     "name": "Assignment 1", "course_id": 1, "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        response = self.client2.put("/api/professors/assignment/1/", {
                                    "name": "Assignment 2", "due_date": "2023-01-01 00:00", "description": "This is an assignment 2"})
        a = Assignment.objects.get(id=1)
        self.assertEqual(a.name, "Assignment 2")
        self.assertEqual(a.description, "This is an assignment 2")
        self.assertEqual(response.status_code, 200)

    def test_raises_error_when_due_date_format_is_wrong(self):
        response = self.client2.post("/api/professors/assignment/", {
                                     "name": "Assignment 1", "course_id": 1, "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        response = self.client2.put("/api/professors/assignment/1/", {
                                    "name": "Assignment 2", "due_date": "2023/01/01", "description": "This is an assignment 2"})
        self.assertEqual(response.status_code, 400)


class TestViewUpdateSubmission(TestCase):
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
        self.client2.post("/api/students/submission/",
                          {"assignment_id": 1, "course_id": 1})
        self.client2.credentials(
            HTTP_AUTHORIZATION='Bearer ' + professor_access)

    def test_update_submission(self):
        response = self.client2.put(
            "/api/professors/submission/1/", {"grade": 100, "grade_comment": "This is a comment"})
        s = Submission.objects.get(id=1)
        self.assertEqual(s.grade, 100)
        self.assertEqual(response.status_code, 200)
