from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from ..serializers import SubmissionSerializer, EnrollmentSerializer
from ..permissions import isStudent, isProfessorAndOwnsCourse, isStudentAndEnrolled
from ..models import Assignment, Course, Student, Enrollment, File


@api_view(["POST"])
@permission_classes([IsAuthenticated, isStudent])
def enroll_student(request):
    """
    Enroll a student in a course
    """
    student = Student.objects.get(user=request.user)
    try: 
        course = Course.objects.get(id=request.data.get("course_id"))
    except:
        return Response({"error": "Course does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = EnrollmentSerializer(data=request.data, context={'student': student, 'course': course})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated, isStudentAndEnrolled])
@parser_classes([MultiPartParser])
def create_submission(request):
    """
    Create a submission
    """
    try:
        assignment = Assignment.objects.get(id=request.data["assignment_id"])
    except:
        return Response({"error": "Assignment does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    student = Student.objects.get(user=request.user)
    data = QueryDict.copy(request.data)
    data["student"] = student
    data["assignment"] = assignment
    serializer = SubmissionSerializer(data=request.data, context={'student': student, 'assignment': assignment})
    if serializer.is_valid():
        submission = serializer.save()
        for file in request.FILES.values():
            file = File.objects.create(
                submission=submission,
                file=file
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)