from django.test import TestCase
from ..models import Professor, Student


class TestViewRegisterProfessor(TestCase):
    def setUp(self) -> None:
        self.client.post('/api/auth/register/professor/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "example@gmail.com", 'password': "password"})

    def test_register_professor(self):
        response = self.client.post('/api/auth/register/professor/', {
                                    'first_name': "John", 'last_name': "Doe", 'email': "example2@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 201)
        professor = Professor.objects.get(user__email="example@gmail.com")
        self.assertEqual(professor.user.first_name, "John")

    def test_raises_error_when_email_already_exists(self):
        response = self.client.post('/api/auth/register/professor/', {
                                    'first_name': "John", 'last_name': "Doe", 'email': "example@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_first_name_is_missing(self):
        response = self.client.post('/api/auth/register/professor/', {
                                    'last_name': "Doe", 'email': "example4@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_last_name_is_missing(self):
        response = self.client.post('/api/auth/register/professor/', {
                                    'first_name': "John", 'email': "example5@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_email_is_missing(self):
        response = self.client.post(
            '/api/auth/register/professor/', {'first_name': "John", 'last_name': "Doe", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_password_is_missing(self):
        response = self.client.post('/api/auth/register/professor/', {
                                    'first_name': "John", 'last_name': "Doe", 'email': "example8@gmail.com"})
        self.assertEqual(response.status_code, 400)

class TestViewRegisterStudent(TestCase):
    def setUp(self) -> None:
        self.client.post('/api/auth/register/student/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "example@gmail.com", 'password': "password"})
    
    def test_register_student(self):
        response = self.client.post('/api/auth/register/student/', {
                                    'first_name': "John", 'last_name': "Doe", 'email': "example2@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 201)
        professor = Student.objects.get(user__email="example@gmail.com")
        self.assertEqual(professor.user.first_name, "John")

    def test_raises_error_when_email_already_exists(self):
        response = self.client.post('/api/auth/register/student/', {
                                    'first_name': "John", 'last_name': "Doe", 'email': "example@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_first_name_is_missing(self):
        response = self.client.post('/api/auth/register/student/', {
                                    'last_name': "Doe", 'email': "example4@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_last_name_is_missing(self):
        response = self.client.post('/api/auth/register/student/', {
                                    'first_name': "John", 'email': "example5@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_email_is_missing(self):
        response = self.client.post(
            '/api/auth/register/professor/', {'first_name': "John", 'last_name': "Doe", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_password_is_missing(self):
        response = self.client.post('/api/auth/register/student/', {
                                    'first_name': "John", 'last_name': "Doe", 'email': "example8@gmail.com"})
        self.assertEqual(response.status_code, 400)