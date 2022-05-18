from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated

from .serializers import CourseSerializer, AssignmentSerializer, SubmissionSerializer, EnrollmentSerializer, UserSerializer
from .permissions import isProfessor, isStudent, isProfessorAndOwnsCourse, isStudentAndEnrolled
from .models import Assignment, Professor, Course, Student, Submission, Enrollment, File, User
from django.utils import timezone
import pytz


@api_view(["POST"])
@permission_classes([IsAuthenticated, isProfessor])
def create_course(request):
    """
    Create a course
    """
    professor = Professor.objects.get(user=request.user)
    course = Course.objects.create(
        name=request.data["name"],
        group=request.data["group"],
        professor=professor
    )

    return Response(CourseSerializer(course).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated, isProfessorAndOwnsCourse])
@parser_classes([MultiPartParser])
def create_assignment(request):
    """
    Create an assignment
    """
    course = Course.objects.get(id=request.data["course_id"])
    # extract the date time year, month, day, hour, minute from the request if due_date has the format "YYYY-MM-DD HH:MM"
    due_date = None
    if "due_date" in request.data:
        try:
            due_date = request.data["due_date"]
            year = int(due_date[0:4])
            month = int(due_date[5:7])
            day = int(due_date[8:10])
            hour = int(due_date[11:13])
            minute = int(due_date[14:16])
            # create a timezone aware datetime object
            due_date = timezone.datetime(year, month, day, hour, minute, tzinfo=pytz.utc)
        except:
            return Response({"error": "Invalid due date format"}, status=400)

    assignment = Assignment.objects.create(
        name=request.data["name"],
        description=request.data["description"],
        due_date=due_date,
        course=course,
    )

    for file in request.FILES.values():
        file = File.objects.create(
            assignment=assignment,
            file=file
        )    

    return Response(AssignmentSerializer(assignment).data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated, isProfessorAndOwnsCourse])
def update_assignment(request, id):
    """
    Update an assignment
    """
    assignment = Assignment.objects.get(id=id)
    # extract the date time year, month, day, hour, minute from the request if due_date has the format "YYYY-MM-DD HH:MM"
    due_date = None
    if "due_date" in request.data:
        try:
            due_date = request.data["due_date"]
            year = int(due_date[0:4])
            month = int(due_date[5:7])
            day = int(due_date[8:10])
            hour = int(due_date[11:13])
            minute = int(due_date[14:16])
            # create a timezone aware datetime object
            due_date = timezone.datetime(year, month, day, hour, minute, tzinfo=pytz.utc)
            assignment.due_date = due_date
        except:
            return Response({"error": "Invalid date format"}, status=400)
    
    if "name" in request.data:
        assignment.name = request.data["name"]
    if "description" in request.data:
        assignment.description = request.data["description"]

    assignment.save()

    return Response(AssignmentSerializer(assignment).data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, isStudent])
def enroll_student(request):
    """
    Enroll a student in a course
    """
    student = Student.objects.get(user=request.user)
    course = Course.objects.get(id=request.data["course_id"])
    period = request.data["period"]
    enrollment = Enrollment.objects.create(
        course=course,
        student=student,
        period=period
    )
    return Response(EnrollmentSerializer(enrollment).data)

@api_view(["POST"])
@permission_classes([IsAuthenticated, isStudentAndEnrolled])
@parser_classes([MultiPartParser])
def create_submission(request):
    """
    Create a submission
    """

    assignment = Assignment.objects.get(id=request.data["assignment_id"])
    student = Student.objects.get(user=request.user)

    submission = Submission.objects.create(
        assignment=assignment,
        student=student,

    )

    for file in request.FILES.values():
        file = File.objects.create(
            assignment=assignment,
            file=file
        )    

    return Response(SubmissionSerializer(submission).data)

@api_view(["PUT"])
@permission_classes([IsAuthenticated, isProfessorAndOwnsCourse])
def update_submission(request, id):
    """
    Update a submission
    """
    submission = Submission.objects.get(id=id)
    if "grade" in request.data:
        submission.grade = request.data["grade"]
        submission.status = Submission.GRADED
    if "grade_comment" in request.data:
        submission.grade_comment = request.data["grade_comment"]
    submission.save()

    return Response(SubmissionSerializer(submission).data)

@api_view(["GET"])
@permission_classes([IsAuthenticated, isProfessorAndOwnsCourse])
def get_students_enrolled_in_course(request):
    """
    Get all students enrolled in a course
    """
    course = Course.objects.get(id=request.data["course_id"])
    enrollments = Enrollment.objects.filter(course=course)
    return Response(EnrollmentSerializer(enrollments, many=True).data)

@api_view(["GET"])
def get_submissions_for_assignment(request, assignment_id):
    """
    Get all submissions for an assignment
    """
    assignment = Assignment.objects.get(id=assignment_id)
    submissions = Submission.objects.filter(assignment=assignment)
    return Response(SubmissionSerializer(submissions, many=True).data)

@api_view(["POST"])
def register_professor(request):
    """
    Register a professor
    """
    user = User.objects.create(
        email=request.data["email"],
        first_name=request.data["first_name"],
        last_name=request.data["last_name"],
        user_type=User.PROFESSOR
    )
    user.set_password(request.data["password"])
    user.save()
    return Response(UserSerializer(user).data)

@api_view(["POST"])
def register_student(request):
    """
    Register a student
    """
    user = User.objects.create(
        email=request.data["email"],
        first_name=request.data["first_name"],
        last_name=request.data["last_name"],
        user_type=User.STUDENT
    )
    user.set_password(request.data["password"])
    user.save()
    return Response(UserSerializer(user).data)


    

