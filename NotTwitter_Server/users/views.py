from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token


# Create your views here.
class Loginout(APIView):
    def post(self, request):
        try:
            username = request.data.get('nickname')
            password = request.data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is None:
                raise AuthenticationFailed('Invalid username or password.')
            
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            usernum = user.id

            return Response(
                {'token': token.key, 'usernum': usernum, 'created': created},
                status=status.HTTP_201_CREATED
            )
        except AuthenticationFailed as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def delete(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise AuthenticationFailed('Authentication credentials were not provided.')
            
            logout(request)
            Token.objects.filter(user=user).delete()

            return Response(
                {'message': 'Logout successful'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class Signupdown(APIView):
    def post(self, request):
        try:
            username = request.data.get('nickname')
            email = request.data.get('mailaddr')
            password = request.data.get('password')

            User.objects.create_user(username=username, email=email, password=password)

            return Response(
                {'message': 'Signup successful'}, 
                status=status.HTTP_201_CREATED
            )
        except IntegrityError as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def delete(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise AuthenticationFailed('Authentication credentials were not provided.')

            user.delete()

            return Response(
                {'message': 'Signdown successful'}, 
                status=status.HTTP_200_OK
            )
        except AuthenticationFailed as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_401_UNAUTHORIZED
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class NicknameView(APIView):
    def get(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise AuthenticationFailed('Authentication credentials were not provided.')

            return Response(
                {'nickname': user.username},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
    def put(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise AuthenticationFailed('Authentication credentials were not provided.')
            
            user.username = request.data.get('nickname')
            user.save()

            return Response(
                {'message': 'Nickname updated successfully.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
