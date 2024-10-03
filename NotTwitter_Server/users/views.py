from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

class Loginout(APIView):
    def post(self, request):
        username = request.data.get('nickname')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        if not user:
            return Response(
                {'error': 'Invalid username or password.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        login(request, user)
        token, created = Token.objects.get_or_create(user=user)

        return Response(
            {'token': token.key, 'usernum': user.id, 'created': created},
            status=status.HTTP_201_CREATED
        )
    def delete(self, request):
        user = request.user
        if user.is_anonymous:
            return Response(
                {'error': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        Token.objects.filter(user=user).delete()
        logout(request)

        return Response(
            {'message': 'Logout successful'}, 
            status=status.HTTP_200_OK
        )


class Signupdown(APIView):
    def post(self, request):
        username = request.data.get('nickname')
        email = request.data.get('mailaddr')
        password = request.data.get('password')
        try:
            User.objects.create_user(username=username, email=email, password=password)
            return Response(
                {'message': 'Signup successful'}, 
                status=status.HTTP_201_CREATED
            )
        except IntegrityError:
            return Response(
                {'error': 'Username or email already exists.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
    def delete(self, request):
        user = request.user
        if user.is_anonymous:
            return Response(
                {'error': 'Authentication credentials were not provided.'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        user.delete()
        return Response(
            {'message': 'Signdown successful'}, 
            status=status.HTTP_200_OK
        )


class NicknameView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        return Response(
            {'nickname': request.user.username},
            status=status.HTTP_200_OK
        )
    def put(self, request):
        user = request.user
        new_nickname = request.data.get('nickname')

        if not new_nickname:
            return Response(
                {'error': 'New nickname is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.username = new_nickname
        user.save()

        return Response(
            {'message': 'Nickname updated successfully.'},
            status=status.HTTP_200_OK
        )
