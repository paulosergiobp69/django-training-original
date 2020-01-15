from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.authentication import TokenAuthentication
from . import views
  
urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
]