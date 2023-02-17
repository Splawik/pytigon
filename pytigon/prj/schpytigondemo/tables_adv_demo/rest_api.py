from django.urls import path
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from oauth2_provider.contrib.rest_framework import TokenHasReadWriteScope

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated, TokenHasReadWriteScope])
def hello_world(request):
    print(request.user)
    if request.method == 'POST':
        return Response({"message": "Got some data!", "data": request.data})
    return Response({"message": "Hello, world!"})


urlpatterns = [
    path("hello", hello_world, name="hello"),
]
