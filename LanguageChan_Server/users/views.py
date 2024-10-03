from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import *
from rest_framework.authtoken.models import Token
from .models import UsersChara, UsersFriends, UsersItem, UsersProgress


class Loginout(APIView):
    def post(self, request):
        try:
            username = request.data.get('nickname')
            password = request.data.get('password')

            user = authenticate(request, username=username, password=password)
            if not user:
                raise AuthenticationFailed('Invalid username or password.')

            login(request, user)
            token, created = Token.objects.get_or_create(user=user)

            return Response(
                {
                    'token': token.key, 
                    'usernum': user.id, 
                    'created': created
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            match type(e):
                case AuthenticationFailed, NotAuthenticated:
                    status_code = status.HTTP_401_UNAUTHORIZED
                case PermissionDenied:
                    status_code = status.HTTP_403_FORBIDDEN
                case Http404:
                    status_code = status.HTTP_404_NOT_FOUND
                case _:
                    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return Response(
                {'error': str(e)}, 
                status=status_code
            )

    def delete(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise AuthenticationFailed('Authentication credentials were not provided.')

            logout(request)
            Token.objects.filter(user=user).delete()
            return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class Signupdown(APIView):
    def post(self, request):
        try:
            username = request.data.get('nickname')
            email = request.data.get('mailaddr')
            password = request.data.get('password')

            User.objects.create_user(username=username, email=email, password=password)
            return Response({'message': 'Signup successful'}, status=status.HTTP_201_CREATED)
        except IntegrityError:
            return Response({'error': 'Username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise AuthenticationFailed('Authentication credentials were not provided.')

            user.delete()
            return Response({'message': 'Account deleted successfully'}, status=status.HTTP_200_OK)
        except AuthenticationFailed as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UsersCharasView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            usernum = request.data.get('usernum')
            charas = UsersChara.objects.filter(usernum=usernum).values_list('charanum', flat=True)
            return Response({'charanums': list(charas)}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UsersCharaView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            usernum = request.data.get('usernum')
            charanum = request.data.get('charanum')
            UsersChara.objects.create(usernum=usernum, charanum=charanum, lvl=1)
            return Response({'message': 'UsersChara created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request):
        try:
            usernum = request.data.get('usernum')
            charanum = request.data.get('charanum')
            chara = UsersChara.objects.get(usernum=usernum, charanum=charanum)
            return Response({'lvl': chara.lvl}, status=status.HTTP_200_OK)
        except UsersChara.DoesNotExist:
            return Response({'error': 'Chara not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self, request):
        try:
            usernum = request.data.get('usernum')
            charanum = request.data.get('charanum')
            lvl = request.data.get('lvl')

            chara = UsersChara.objects.get(usernum=usernum, charanum=charanum)
            chara.lvl = lvl
            chara.save()
            return Response({'message': 'UsersChara updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UsersFriendsView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            usernum = request.data.get('usernum')
            friendnum = request.data.get('friendnum')
            UsersFriends.objects.create(usernum=usernum, friendnum=friendnum)
            return Response({'message': 'UsersFriends created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def delete(self, request):
        try:
            usernum = request.data.get('usernum')
            friendnum = request.data.get('friendnum')
            UsersFriends.objects.get(usernum=usernum, friendnum=friendnum).delete()
            return Response({'message': 'UsersFriends deleted successfully'}, status=status.HTTP_200_OK)
        except UsersFriends.DoesNotExist:
            return Response({'error': 'Friendship not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UsersItemView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            usernum = request.data.get('usernum')
            usersitem, created = UsersItem.objects.get_or_create(
                usernum=usernum, defaults={'money': 100, 'jewel': 10}
            )
            if created:
                return Response({'message': 'UsersItem created successfully'}, status=status.HTTP_201_CREATED)
            return Response({'message': 'UsersItem already exists'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request):
        try:
            usernum = request.data.get('usernum')
            item = UsersItem.objects.get(usernum=usernum)
            return Response({'money': item.money, 'jewel': item.jewel}, status=status.HTTP_200_OK)
        except UsersItem.DoesNotExist:
            return Response({'error': 'Item not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self, request):
        try:
            usernum = request.data.get('usernum')
            money = request.data.get('money')
            jewel = request.data.get('jewel')

            item = UsersItem.objects.get(usernum=usernum)
            item.money = money
            item.jewel = jewel
            item.save()
            return Response({'message': 'UsersItem updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UsersProgressView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            usernum = request.data.get('usernum')
            lessonmapnum = request.data.get('lessonmapnum')
            UsersProgress.objects.create(usernum=usernum, lessonmapnum=lessonmapnum, progress=1)
            return Response({'message': 'UsersProgress created successfully'}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request):
        try:
            usernum = request.data.get('usernum')
            lessonmapnum = request.data.get('lessonmapnum')
            progress = UsersProgress.objects.get(usernum=usernum, lessonmapnum=lessonmapnum).progress
            return Response({'progress': progress}, status=status.HTTP_200_OK)
        except UsersProgress.DoesNotExist:
            return Response({'error': 'Progress not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def put(self, request):
        try:
            usernum = request.data.get('usernum')
            lessonmapnum = request.data.get('lessonmapnum')
            progress = request.data.get('progress')

            progress_record = UsersProgress.objects.get(usernum=usernum, lessonmapnum=lessonmapnum)
            progress_record.progress = progress
            progress_record.save()
            return Response({'message': 'UsersProgress updated successfully'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': 'An error occurred.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
