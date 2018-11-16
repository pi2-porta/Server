from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_jwt.settings import api_settings

# from .decorators import validate_request_data
from .models import Registros
from .models import Profile
from .serializers import RegistrosSerializer, TokenSerializer, UserSerializer

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from .serializers import RegistrosSerializer
from .decorators import validate_request_data

#face recognition
import face_recognition

#system
import sys

class ListCreateRegistrosView(generics.ListCreateAPIView):
    """
    GET songs/
    POST songs/
    """
    queryset = Registros.objects.all()
    serializer_class = RegistrosSerializer
    permission_classes = (permissions.IsAuthenticated,)

    @validate_request_data
    def post(self, request, *args, **kwargs):
        r = Registros.objects.create(
            title=request.data["title"],
            description=request.data["description"],
            author=request.user
        )
        
        return Response(
            data=RegistrosSerializer(r).data,
            status=status.HTTP_201_CREATED
        )

class LoginView(generics.CreateAPIView):
    """
    POST auth/login/
    """
    # This permission class will overide the global permission
    # class setting
    permission_classes = (permissions.AllowAny,)

    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # login saves the user’s ID in the session,
            # using Django’s session framework.
            login(request, user)
            serializer = TokenSerializer(data={
                # using drf jwt utility functions to generate a token
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )})
            serializer.is_valid()
            return Response(serializer.data)
        return Response(status=status.HTTP_401_UNAUTHORIZED)

class RegisterUsersView(generics.CreateAPIView):
    """
    POST auth/register/
    """
    permission_classes = (permissions.AllowAny,)

    def post(self, request, *args, **kwargs):
        username = request.data.get("username", "")
        password = request.data.get("password", "")
        email = request.data.get("email", "")
        photo = request.data.get("photo")
        
        if not username and not password and not email:
            return Response(
                data={
                    "message": "username, password and email is required to register a user"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        new_user = User.objects.create_user(
            username=username, password=password, email=email
        )

        new_user.profile.image = photo
       

        new_face = face_recognition.load_image_file(new_user.profile.image.path)

        try:
             new_face_encoding = face_recognition.face_encodings(new_face)[0]
        
        except IndexError:
            print("I wasn't able to locate any faces in at least one of the images. Check the image files. Aborting...")
            # quit()

        print(new_face_encoding)

        new_user.profile.encode = new_face_encoding


        #####



        #####







        new_user.save()

        return Response(status=status.HTTP_201_CREATED)