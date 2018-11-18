from django.urls import path
from .views import ListCreateRegistrosView
from .views import LoginView
from .views import RegisterUsersView
from .views import SearchUserPhotoView


urlpatterns = [
    path('registros/', ListCreateRegistrosView.as_view(), name="registros-all"),
    path('search/', SearchUserPhotoView.as_view(), name="search" ),
    path('auth/login/', LoginView.as_view(), name="auth-login"),
    path('auth/register/', RegisterUsersView.as_view(), name="auth-register")

]
