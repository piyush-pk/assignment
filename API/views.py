from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from .serializer import *
from django.contrib.auth import get_user_model
User = get_user_model()



@api_view(['POST'])
def register(request):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated, )
    serial = UserSerializer(data = request.data)
    if not serial.is_valid():
        return Response({"status": status.HTTP_400_BAD_REQUEST, "error": serial.errors})
    serial.save()
    user = User.objects.get(email = serial.data['email'])
    refresh = RefreshToken.for_user(user)
    return Response({"status": status.HTTP_201_CREATED, "payload": serial.data, 'refresh': str(refresh),
    'access': str(refresh.access_token)})


###################################################################################################

# @api_view(['PATCH'])
# def update(request):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = (IsAuthenticated, )
#     user = User.objects.get(email = request.data['email'])
#     serial = UserSerializer(user)
#     refresh = RefreshToken.for_user(user)
#     return Response({"status": 200, "payload": serial.data, 'refresh': str(refresh),
#     'access': str(refresh.access_token),})

@api_view(['GET'])
def profile(request):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated, )
    user = User.objects.get(id = request.data['id'])
    serial = UserSerializer(user)
    refresh = RefreshToken.for_user(user)
    return Response({"status": 200, "payload": serial.data, 'refresh': str(refresh),
    'access': str(refresh.access_token),})



@api_view(['PATCH'])
def update(request, id):
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated, )
    user = User.objects.get(id = id)
    serial = UserSerializer(user, data = request.data, partial = True)

    if not serial.is_valid():
        return Response({"status": status.HTTP_400_BAD_REQUEST, "errors": serial.errors})

    serial.save()
    # print(user)
    return Response({"status": status.HTTP_201_CREATED, "data": serial.data, "message": "updated Successfully"})


@api_view(['DELETE'])
def delete(request):
    try:
        user = User.objects.get(id = request.data['id'])
        user.delete()
        # serial = ProfileSerializer(user)
        # # print(request.data['id'],)
        return Response({"status": status.HTTP_200_OK, "message": "user deleted successfully"})

    except Exception as e:

        return Response({"error": "Something wents Wrong"})