from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import isProfessor, isProfessorAndOwnsCourse
from .models import Assignment, Professor, Course
from django.utils import timezone
import pytz

@api_view(["POST"])
@permission_classes([IsAuthenticated, isProfessorAndOwnsCourse])
def create_assignment(request):
    """
    Create an assignment
    """
    course = Course.objects.get(id=request.data["course_id"])
    # extract the date time year, month, day, hour, minute from the request if due_date has the format "YYYY-MM-DD HH:MM"
    due_date = None
    if "due_date" in request.data:
        due_date = request.data["due_date"]
        year = int(due_date[0:4])
        month = int(due_date[5:7])
        day = int(due_date[8:10])
        hour = int(due_date[11:13])
        minute = int(due_date[14:16])
        # create a timezone aware datetime object
        due_date = timezone.datetime(year, month, day, hour, minute, tzinfo=pytz.utc)

    assignment = Assignment.objects.create(
        name=request.data["name"],
        description=request.data["description"],
        due_date=due_date,
        course=course,
    )
    assignment.save()

    return Response({"id": assignment.id, "name": assignment.name, "description": assignment.description, "due_date": assignment.due_date, "course_id": assignment.course.id})

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
    course.save()

    return Response({"id": course.id, "name": course.name, "group": course.group})

