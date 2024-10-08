from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import *
from rest_framework.authtoken.models import Token


# 보안용 유저 검증하는 함수
def user_check(user):
    if user.is_anonymous:
        raise AuthenticationFailed('User is not authenticated.')
    if not User.objects.filter(id=user.id).exists():
        raise AuthenticationFailed('User does not exist.')

# 예외 Response객체 팩토리 함수
def make_exception_response(e):
    if isinstance(e, APIException):
        status_code=e.status_code
    else:
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    return Response(
        {'error': str(e)},
        status=status_code
    )


class Loginout(APIView):
    def post(self, request):
        try:
            username = request.data.get('nickname')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
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
            return make_exception_response(e)
    def delete(self, request):
        try:
            user = request.user
            user_check(user)

            Token.objects.filter(user=user).delete()
            logout(request)

            return Response(
                {'message': 'Logout successful'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return make_exception_response(e)

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
            return make_exception_response(e)
    def delete(self, request):
        try:
            user = request.user
            user_check(user)

            user.delete()

            return Response(
                {'message': 'Signdown successful'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return make_exception_response(e)

class NicknameView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            user_check(user)

            return Response(
                {'nickname': request.user.username},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return make_exception_response(e)
    def put(self, request):
        try:
            user = request.user
            user_check(user)

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
            return make_exception_response(e)
