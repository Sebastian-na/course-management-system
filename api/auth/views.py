from django.http import QueryDict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from ..serializers import UserSerializer
from ..models import User


@api_view(["POST"])
def register_professor(request):
    """
    Register a professor
    """
    data = QueryDict.copy(request.data)
    data['user_type'] = User.PROFESSOR
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def register_student(request):
    """
    Register a student
    """
    data = QueryDict.copy(request.data)
    data['user_type'] = User.STUDENT
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
