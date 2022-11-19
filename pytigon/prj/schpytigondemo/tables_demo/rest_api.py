from django.urls import path
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET','POST'])
def hello_world(request):
        if request.method == 'POST':
                return Response({"message": "Got some data2!", "data": request.data})
        return Response({"message": "Hello, world2!"})


urlpatterns = [
    path("hello2", hello_world, name="hello2"),
]
