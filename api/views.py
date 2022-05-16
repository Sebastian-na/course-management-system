from rest_framework.response import Response
from rest_framework.decorators import api_view

@api_view(["GET"])
def test():
    data = {
        "message": "Hello World"
    }
    return Response(data)


# Create your views here.
