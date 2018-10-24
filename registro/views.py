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
from .serializers import RegistrosSerializer, TokenSerializer, UserSerializer

# Get the JWT settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

from .serializers import RegistrosSerializer
from .decorators import validate_request_data

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
        a_song = Registros.objects.create(
            title=request.data["title"],
            description=request.data["description"]
        )
        return Response(
            data=RegistrosSerializer(a_song).data,
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
        return Response(status=status.HTTP_201_CREATED)