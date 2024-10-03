from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.authtoken.models import Token

from .models import *

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


class UsersCharasView(APIView):
    def get(self, request):
        try:
            usernum = request.data.get('usernum')
            charas = UsersChara.objects.values('charanum').filter(usernum=usernum)

            data = {'charanums': [chara.get('charanum') for chara in charas]}
            return Response(
                data,
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UsersCharaView(APIView):
    def post(self, request):
        try:
            usernum = request.data.get('usernum')
            charanum = request.data.get('charanum')
            lvl = 1

            UsersChara.objects.create(usernum=usernum, charanum=charanum, lvl=lvl)
            return Response(
                {'message': 'UsersChara created successfully'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def get(self, request):
        try:
            usernum = request.data.get('usernum')
            charanum = request.data.get('charanum')
            chara = UsersChara.objects.get(usernum=usernum, charanum=charanum)

            return Response(
                {'lvl': chara.lvl},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def put(self, request):
        try:
            usernum = request.data.get('usernum')
            charanum = request.data.get('charanum')
            lvl = request.data.get('lvl')

            chara = UsersChara.objects.get(usernum=usernum, charanum=charanum)
            chara.lvl = lvl
            chara.save()

            return Response(
                {'message': 'UsersChara updated successfully'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UsersFriendsView(APIView):
    def post(self, request):
        try:
            usernum = request.data.get('usernum')
            friendnum = request.data.get('friendnum')

            UsersFriends.objects.create(usernum=usernum, friendnum=friendnum)
            return Response(
                {'message': 'UsersFriends created successfully'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def delete(self, request):
        try:
            usernum = request.data.get('usernum')
            friendnum = request.data.get('friendnum')

            friendship = UsersFriends.objects.get(usernum=usernum, friendnum=friendnum)
            friendship.delete()
            
            return Response(
                {'message': 'UsersFriends deleted successfully'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UsersItemView(APIView):
    def post(self, request):
        try:
            usernum = request.data.get('usernum')
            money = 100
            jewel = 10

            usersitem, created = UsersItem.objects.get_or_create(
                usernum=usernum, 
                defaults={'money': money, 'jewel': jewel}
            )

            if created:
                return Response(
                    {'message': 'Usersitem created successfully'}, 
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'message': 'Usersitem already exists'}, 
                    status=status.HTTP_200_OK
                )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def get(self, request):
        try:
            usernum = request.data.get('usernum')

            item = UsersItem.objects.get(usernum=usernum)
            return Response(
                {
                    'money': item.money, 
                    'jewel': item.jewel
                }, 
                status=status.HTTP_200_OK
            )
        except UsersItem.DoesNotExist as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def put(self, request):
        try:
            usernum = request.data.get('usernum')
            money = request.data.get('money')
            jewel = request.data.get('jewel')

            item = UsersItem.objects.get(usernum=usernum)
            item.money = money
            item.jewel = jewel
            item.save()

            return Response(
                {'message': 'Usersitem updated successfully'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class UsersProgressView(APIView):
    def post(self, request):
        try:
            usernum = request.data.get('usernum')
            lessonmapnum = request.data.get('lessonmapnum')
            progress = 1

            UsersProgress.objects.create(usernum=usernum, lessonmapnum=lessonmapnum, progress=progress)
            return Response(
                {'message': 'UsersProgress created successfully'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def get(self, request):
        try:
            usernum = request.data.get('usernum')
            lessonmapnum = request.data.get('lessonmapnum')

            progress_record = UsersProgress.objects.get(usernum=usernum, lessonmapnum=lessonmapnum)
            return Response(
                {'progress': progress_record.progress}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def put(self, request):
        try:
            usernum = request.data.get('usernum')
            lessonmapnum = request.data.get('lessonmapnum')
            progress = request.data.get('progress')

            progress_record = UsersProgress.objects.get(usernum=usernum, lessonmapnum=lessonmapnum)
            progress_record.progress = progress
            progress_record.save()
            
            return Response(
                {'message': 'UsersProgress updated successfully'}, 
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
