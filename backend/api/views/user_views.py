from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework import status

from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.serializers import Serializer

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from api.models import *
from api.serializers import Userserializer,UserserializerWithToken

class MyTokenObtainPairserializer(TokenObtainPairSerializer):
    def validate(self , attrs):
        data = super().validate(attrs) #for validation token
        serializer = UserserializerWithToken(self.user).data
        for k,v in serializer.items():
            data[k] = v
        return data
    
    @classmethod
    def get_token(cls , user):
        token = super.get_token(user)

        #addd customer claims
        token['username'] = user.username
        token['message'] = "Hello Proshop"

        return token
    

class MyTokenObtainPairView(TokenObtainPairView):
    
    Serializer_class = MyTokenObtainPairserializer

@api_view(['GET'])
def getRoutes(request):
    routes = [
        '/api/products/',
        '/api/products/<id>',
        '/api/users',
        '/api/users/register',
        '/api/users/login',
        '/api/user/profile',
    ]
    return Response(routes)

@api_view(['POST'])
def registerUser(request):
    data = request.data
    try:
        user = User.objects.create(
         first_name = data['name'],
         username = data['email'],
         password = make_password(data['password']),
        )
        Serializer = UserserializerWithToken(user, many=False)
        return Response(Serializer.data)
    except:
        message = {'detail':'user with this email is already registered'}
        return Response(message,status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    Serializer = Userserializer(user , many=False)
    return Response(Serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def updateUserProfile(request):
    user = request.user
    Serializer = UserserializerWithToken(user , many=  False)
    data = request.data 
    user.first_name = data['name']
    user.username = data['email']
    user.email = data['email']
    if data['password'] !="":
        user.password = make_password(data['password'])
    user.save()
    return Response(Serializer.data)


@api_view(['DELETE'])
@permission_classes(IsAuthenticated)
def deleteUser(request,pk):
    user = User.objects.get(id=pk)
    user.delete()
    return Response("user is deleted")