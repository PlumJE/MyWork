from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import *
from rest_framework.authtoken.models import Token


class Loginout(APIView):
    def post(self, request):
        try:
            username = request.data.get('nickname')
            password = request.data.get('password')

            user = authenticate(request, username=username, password=password)
            if not user:
                raise AuthenticationFailed('Nickname or password is incorrect.')

            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    'token': token.key, 
                    'usernum': user.id, 
                    'created': created
                },
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            if isinstance(e, APIException):
                status_code=e.status_code
            else:
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(
                {'error': str(e)},
                status=status_code
            )
    def delete(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise NotAuthenticated('Authentication credentials were not provided.')

            Token.objects.filter(user=user).delete()
            logout(request)

            return Response(
                {'message': 'Logout successful'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            if isinstance(e, APIException):
                status_code=e.status_code
            else:
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(
                {'error': str(e)},
                status=status_code
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
        except Exception as e:
            if isinstance(e, APIException):
                status_code=e.status_code
            else:
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(
                {'error': str(e)},
                status=status_code
            )
    def delete(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise NotAuthenticated('Authentication credentials were not provided.')

            user.delete()
            return Response(
                {'message': 'Signdown successful'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            if isinstance(e, APIException):
                status_code=e.status_code
            else:
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(
                {'error': str(e)},
                status=status_code
            )


class NicknameView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            return Response(
                {'nickname': request.user.username},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            if isinstance(e, APIException):
                status_code=e.status_code
            else:
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(
                {'error': str(e)},
                status=status_code
            )
    def put(self, request):
        try:
            user = request.user
            new_nickname = request.data.get('nickname')

            if not new_nickname:
                raise ValidationError('Nickname is required.')

            if User.objects.filter(username=new_nickname).exists():
                raise ValidationError('Nickname already exists.')

            user.username = new_nickname
            user.save()

            return Response(
                {'message': 'Nickname updated successfully.'},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            if isinstance(e, APIException):
                status_code=e.status_code
            else:
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(
                {'error': str(e)},
                status=status_code
            )
