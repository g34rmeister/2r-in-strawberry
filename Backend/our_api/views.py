from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets

# Create your views here.
class LoginView(APIView):
    #call on post request to login
    def post(self, request, *args, **kwargs):
        #retrieve the username and password
        username = request.data.get('username')
        password = request.data.get('password')

        #use built in django login
        user = authenticate(request, username=username, password=password)

        if user is not None:
            #user sent valid login info
            #login the user
            login(request, user)
            #return the response for login as json
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email
            }, status=status.HTTP_200_OK)#tell axios it was a success
        else:
            #login invalid
            return Response(
                {'error': 'Invalid Credentials'},
                status=status.HTTP_400_BAD_REQUEST
            )