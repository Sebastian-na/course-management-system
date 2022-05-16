import profile
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .permissions import isProfessor
from .models import Assignment, Professor, Course

@api_view(["POST"])
@permission_classes([IsAuthenticated, isProfessor])
def create_assignment(request):
    """
    Create an assignment
    """

    print(request.data)
    professor_id = Professor.objects.get(user=request.user).id
    assignment = Assignment.objects.create(
        name=request.data["name"],
        description=request.data["description"],
        expires_at=request.data["expires_at"],
        course=request.data["course"],
        professor=professor_id
    )
    assignment.save()

    return Response({"id": assignment.id})

@api_view(["POST"])
@permission_classes([IsAuthenticated, isProfessor])
def create_course(request):
    """
    Create a course
    """

    print(request.data)
    professor_id = Professor.objects.get(user=request.user).id
    course = Course.objects.create(
        name=request.data["name"],
        group=request.data["group"],
        professor=professor_id
    )
    course.save()

    return Response({"id": course.id})


    


# Create your views here.
