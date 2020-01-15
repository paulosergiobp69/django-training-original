from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import views
from .serializers import UserSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate

# Create your views here.
class DefaultModelViewSet(viewsets.ModelViewSet):

    def dispatch(self, request, *args, **kwargs):
        response = super(DefaultModelViewSet, self).dispatch(
            request, *args, **kwargs)
        if request.user.id:
            token = Token.objects.get(user=request.user)
            # print(token.key)
            response['Token'] = token.key
            return response
        else:
            return response

class UserAPI(DefaultModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class LoginView(views.APIView):
    permission_classes = ()
    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)
