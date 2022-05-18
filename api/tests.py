from django.test import TestCase
from rest_framework.test import APIClient
from .models import Professor, Student, Course, Assignment, Enrollment, Submission


class TestViewRegisterProfessor(TestCase):
    def setUp(self) -> None:
        self.client.post('/api/register/professor/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "example@gmail.com", 'password': "password"})

    def test_register_professor(self):
        response = self.client.post('/api/register/professor/', {
                                    'first_name': "John", 'last_name': "Doe", 'email': "example2@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 201)
        professor = Professor.objects.get(user__email="example@gmail.com")
        self.assertEqual(professor.user.first_name, "John")

    def test_raises_error_when_email_already_exists(self):
        response = self.client.post('/api/register/professor/', {
                                    'first_name': "John", 'last_name': "Doe", 'email': "example@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_first_name_is_missing(self):
        response = self.client.post('/api/register/professor/', {
                                    'last_name': "Doe", 'email': "example4@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_last_name_is_missing(self):
        response = self.client.post('/api/register/professor/', {
                                    'first_name': "John", 'email': "example5@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_email_is_missing(self):
        response = self.client.post(
            '/api/register/professor/', {'first_name': "John", 'last_name': "Doe", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_password_is_missing(self):
        response = self.client.post('/api/register/professor/', {
                                    'first_name': "John", 'last_name': "Doe", 'email': "example8@gmail.com"})
        self.assertEqual(response.status_code, 400)

class TestViewRegisterStudent(TestCase):
    def setUp(self) -> None:
        self.client.post('/api/register/student/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "example@gmail.com", 'password': "password"})
    
    def test_register_student(self):
        response = self.client.post('/api/register/student/', {
                                    'first_name': "John", 'last_name': "Doe", 'email': "example2@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 201)
        professor = Student.objects.get(user__email="example@gmail.com")
        self.assertEqual(professor.user.first_name, "John")

    def test_raises_error_when_email_already_exists(self):
        response = self.client.post('/api/register/student/', {
                                    'first_name': "John", 'last_name': "Doe", 'email': "example@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_first_name_is_missing(self):
        response = self.client.post('/api/register/student/', {
                                    'last_name': "Doe", 'email': "example4@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_last_name_is_missing(self):
        response = self.client.post('/api/register/student/', {
                                    'first_name': "John", 'email': "example5@gmail.com", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_email_is_missing(self):
        response = self.client.post(
            '/api/register/professor/', {'first_name': "John", 'last_name': "Doe", 'password': "password"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_password_is_missing(self):
        response = self.client.post('/api/register/student/', {
                                    'first_name': "John", 'last_name': "Doe", 'email': "example8@gmail.com"})
        self.assertEqual(response.status_code, 400)

class TestViewCreateCourse(TestCase):
    client2 = APIClient() 
    def setUp(self) -> None:
        self.client.post('/api/register/professor/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "professor@gmail.com", 'password': "password"})
        response = self.client.post('/api/token/', {'email': "professor@gmail.com", 'password': "password"})
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
    def test_create_course(self):
        response = self.client2.post('/api/create/course/', {
                                    'name': "Math", 'group': 8})
        c = Course.objects.get(id=1)
        self.assertEqual(c.name, "Math")
        self.assertEqual(response.status_code, 201)

    def test_raises_error_when_name_is_missing(self):
        response = self.client2.post('/api/create/course/', {
                                    'group': 8})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_group_is_missing(self):
        response = self.client2.post('/api/create/course/', {
                                    'name': "Math"})
        self.assertEqual(response.status_code, 400)
    


class TestViewCreateAssignment(TestCase):
    client2 = APIClient() 
    course_id: int
    def setUp(self) -> None:
        self.client.post('/api/register/professor/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "professor@gmail.com", 'password': "password"})
        response = self.client.post('/api/token/', {'email': "professor@gmail.com", 'password': "password"})
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        course = self.client2.post("/api/create/course/", {
                         'name': "Math", 'group': 8})  

    def test_create_assignment(self):
        response = self.client2.post("/api/create/assignment/", {"name": "Assignment 1", "course_id": 1, "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        a = Assignment.objects.get(id=1)
        self.assertEqual(a.name, "Assignment 1")
        self.assertEqual(response.status_code, 201)

    def test_raises_error_when_name_is_missing(self):
        response = self.client2.post("/api/create/assignment/", {"course_id": 1, "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        self.assertEqual(response.status_code, 400)
    
    def test_raises_error_when_course_id_is_missing(self):
        response = self.client2.post("/api/create/assignment/", {"name": "Assignment 1", "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        self.assertEqual(response.status_code, 400)
    
    def test_raises_error_when_due_date_is_missing(self):
        response = self.client2.post("/api/create/assignment/", {"name": "Assignment 1", "course_id": 1, "description": "This is an assignment"})
        self.assertEqual(response.status_code, 400)
    
    def test_raises_error_when_description_is_missing(self):
        response = self.client2.post("/api/create/assignment/", {"name": "Assignment 1", "course_id": 1, "due_date": "2023-01-01 00:00"})
        self.assertEqual(response.status_code, 400)
    
    def test_raises_error_when_course_id_does_not_exist(self):
        response = self.client2.post("/api/create/assignment/", {"name": "Assignment 1", "course_id": 2, "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        self.assertEqual(response.status_code, 400)
    
    def test_raises_error_when_due_date_is_in_the_past(self):
        response = self.client2.post("/api/create/assignment/", {"name": "Assignment 1", "course_id": 1, "due_date": "2020-01-01 00:00", "description": "This is an assignment"})
        self.assertEqual(response.status_code, 400)

    def test_raises_error_when_due_date_format_is_wrong(self):
        response = self.client2.post("/api/create/assignment/", {"name": "Assignment 1", "course_id": 1, "due_date": "2023/01/01", "description": "This is an assignment"})
        self.assertEqual(response.status_code, 400)
    
class TestViewUpdateAssignment(TestCase):
    client2 = APIClient() 
    def setUp(self) -> None:
        self.client.post('/api/register/professor/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "professor@gmail.com", 'password': "password"})
        response = self.client.post('/api/token/', {'email': "professor@gmail.com", 'password': "password"})
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        course = self.client2.post("/api/create/course/", {
                         'name': "Math", 'group': 8})  

    def test_update_assignment(self):
        response = self.client2.post("/api/create/assignment/", {"name": "Assignment 1", "course_id": 1, "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        response = self.client2.put("/api/update/assignment/1/", {"name": "Assignment 2", "due_date": "2023-01-01 00:00", "description": "This is an assignment 2"})
        a = Assignment.objects.get(id=1)
        self.assertEqual(a.name, "Assignment 2")
        self.assertEqual(a.description, "This is an assignment 2")
        self.assertEqual(response.status_code, 200)
    
    def test_raises_error_when_due_date_format_is_wrong(self):
        response = self.client2.post("/api/create/assignment/", {"name": "Assignment 1", "course_id": 1, "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        response = self.client2.put("/api/update/assignment/1/", {"name": "Assignment 2", "due_date": "2023/01/01", "description": "This is an assignment 2"})
        self.assertEqual(response.status_code, 400)

class TestViewEnrollStudent(TestCase):
    client2 = APIClient() 
    def setUp(self) -> None:
        self.client.post('/api/register/professor/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "professor@gmail.com", 'password': "password"})
        self.client.post('/api/register/student/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "example@gmail.com", 'password': "password"})
        professor_access = self.client.post('/api/token/', {'email': "professor@gmail.com", 'password': "password"}).data.get("access")
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + professor_access)
        course = self.client2.post("/api/create/course/", {
                            'name': "Math", 'group': 8})
        
        student_access = self.client.post('/api/token/', {'email': "example@gmail.com", 'password': 'password'}).data.get("access")
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + student_access)

    def test_enroll_student(self):
        response = self.client2.post("/api/enroll/student/", {"course_id": 1, "period": 20222})
        e = Enrollment.objects.get(student_id=1, course_id=1)
        self.assertEqual(e.period, 20222)
        self.assertEqual(response.status_code, 201)

    def test_raises_error_when_course_id_is_missing(self):
        response = self.client2.post("/api/enroll/student/", {"period": 20222})
        self.assertEqual(response.status_code, 400)
    
    def test_raises_error_when_period_is_missing(self):
        response = self.client2.post("/api/enroll/student/", {"course_id": 1})
        self.assertEqual(response.status_code, 400)
    
    def test_raises_error_when_course_id_does_not_exist(self):
        response = self.client2.post("/api/enroll/student/", {"course_id": 2, "period": 20222})
        self.assertEqual(response.status_code, 400)
    
    def test_raises_error_when_period_format_is_wrong(self):
        response = self.client2.post("/api/enroll/student/", {"course_id": 1, "period": 20223})
        self.assertEqual(response.status_code, 400)

class TestViewCreateSubmission(TestCase):
    client2 = APIClient() 
    def setUp(self) -> None:
        self.client.post('/api/register/professor/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "professor@gmail.com", 'password': "password"})
        self.client.post('/api/register/student/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "example@gmail.com", 'password': "password"})
        professor_access = self.client.post('/api/token/', {'email': "professor@gmail.com", 'password': "password"}).data.get("access")
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + professor_access)
        course = self.client2.post("/api/create/course/", {
                            'name': "Math", 'group': 8})
        assignment = self.client2.post("/api/create/assignment/", {"name": "Assignment 1", "course_id": 1, "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        
        student_access = self.client.post('/api/token/', {'email': "example@gmail.com", 'password': 'password'}).data.get("access")
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + student_access)
        self.client2.post("/api/enroll/student/", {"course_id": 1, "period": 20222})

    def test_create_submission(self):

        response = self.client2.post("/api/create/submission/", {"assignment_id": 1, "course_id": 1})
        a = Assignment.objects.get(id=1)
        s = Student.objects.get(id=1)
        su = Submission.objects.filter(assignment=a, student=s)
        self.assertEqual(response.status_code, 201)
    
    def test_raises_error_when_assignment_id_is_missing(self):
        response = self.client2.post("/api/create/submission/", {"course_id": 1})
        self.assertEqual(response.status_code, 400)
    
    def test_raises_error_when_assignment_id_does_not_exist(self):
        response = self.client2.post("/api/create/submission/", {"assignment_id": 2, "course_id": 1})
        self.assertEqual(response.status_code, 400)

class TestViewUpdateSubmission(TestCase):
    client2 = APIClient() 
    def setUp(self) -> None:
        self.client.post('/api/register/professor/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "professor@gmail.com", 'password': "password"})
        self.client.post('/api/register/student/', {
                         'first_name': "John", 'last_name': "Doe", 'email': "example@gmail.com", 'password': "password"})
        professor_access = self.client.post('/api/token/', {'email': "professor@gmail.com", 'password': "password"}).data.get("access")
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + professor_access)
        course = self.client2.post("/api/create/course/", {
                            'name': "Math", 'group': 8})
        assignment = self.client2.post("/api/create/assignment/", {"name": "Assignment 1", "course_id": 1, "due_date": "2023-01-01 00:00", "description": "This is an assignment"})
        
        student_access = self.client.post('/api/token/', {'email': "example@gmail.com", 'password': 'password'}).data.get("access")
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + student_access)
        self.client2.post("/api/enroll/student/", {"course_id": 1, "period": 20222})
        self.client2.post("/api/create/submission/", {"assignment_id": 1, "course_id": 1})
        self.client2.credentials(HTTP_AUTHORIZATION='Bearer ' + professor_access)

    def test_update_submission(self):
        response = self.client2.put("/api/update/submission/1/", {"grade": 100, "grade_comment": "This is a comment"})
        s = Submission.objects.get(id=1)
        self.assertEqual(s.grade, 100)
        self.assertEqual(response.status_code, 200)

        
    
    

    


    
        
        