from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["POST"])
def create_assignment(request):
    print(request.data)
    return Response({"message": "create_assignment"})
    


# Create your views here.
