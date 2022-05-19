from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..serializers import CourseSerializer, AssignmentSerializer, SubmissionSerializer, EnrollmentSerializer
from ..permissions import isProfessor, isProfessorAndOwnsCourse
from ..models import Assignment, Professor, Course, File, Submission, Enrollment

@api_view(["POST"])
@permission_classes([IsAuthenticated, isProfessor])
def create_course(request):
    """
    Create a course
    """
    professor = Professor.objects.get(user=request.user)
    data = QueryDict.copy(request.data)
    data['professor'] = professor
    serializer = CourseSerializer(data=data, context={'professor': professor})
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([IsAuthenticated, isProfessorAndOwnsCourse])
@parser_classes([MultiPartParser])
def create_assignment(request):
    """
    Create an assignment
    """
    try:
        course = Course.objects.get(id=request.data.get("course_id"))
    except:
        return Response({"error": "Course does not exist"}, status=status.HTTP_400_BAD_REQUEST)

    data = QueryDict.copy(request.data)
    data['course'] = course
    serializer = AssignmentSerializer(data=data, context={'course': course})
    if serializer.is_valid():
        assignment = serializer.save()
        for file in request.FILES.values():
            file = File.objects.create(
                assignment=assignment,
                file=file
            )
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAuthenticated, isProfessorAndOwnsCourse])
def update_assignment(request, id):
    """
    Update an assignment
    """
    assignment = Assignment.objects.get(id=id)
    serializer = AssignmentSerializer(assignment, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PUT"])
@permission_classes([IsAuthenticated, isProfessorAndOwnsCourse])
def update_submission(request, id):
    """
    Update a submission
    """
    try:
        submission = Submission.objects.get(id=id)
    except:
        return Response({"error": "Submission does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    
    serializer = SubmissionSerializer(submission, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET"])
@permission_classes([IsAuthenticated, isProfessor])
def get_submissions_for_assignment(request, assignment_id):
    """
    Get all submissions for an assignment
    """
    try:
        assignment = Assignment.objects.get(id=assignment_id)
    except:
        return Response({"error": "Assignment does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    submissions = Submission.objects.filter(assignment=assignment)
    return Response(SubmissionSerializer(submissions, many=True).data)

@api_view(["GET"])
@permission_classes([IsAuthenticated, isProfessorAndOwnsCourse])
def get_students_enrolled_in_course(request):
    """
    Get all students enrolled in a course
    """
    try:
        course = Course.objects.get(id=request.data["course_id"])
    except:
        return Response({"error": "Course does not exist"}, status=status.HTTP_400_BAD_REQUEST)
    enrollments = Enrollment.objects.filter(course=course)
    return Response(EnrollmentSerializer(enrollments, many=True).data)