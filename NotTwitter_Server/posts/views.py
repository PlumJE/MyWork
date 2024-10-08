from django.contrib.auth.models import User
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import *

from .models import *


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

# 새로운 id를 만드는 함수
def generate_new_id(id_prefix):
    id_regex = f"^{id_prefix}/[0-9]+$" if id_prefix else '^[0-9]+$'
    new_id_suffix = Posts.objects.filter(id__regex=id_regex).count()

    if id_prefix:
        return f"{id_prefix}/{new_id_suffix}"
    return str(new_id_suffix)


class PostlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            user_check(user)

            id_prefix = request.data.get('id_prefix', '')
            id_regex = f"^{id_prefix}(/[0-9]+)?$" if id_prefix else '^[0-9]+$'
            
            posts = Posts.objects.filter(id__regex=id_regex).values_list('id', flat=True)
            if not posts.exists():
                raise NotFound('No posts found with the given prefix')
            
            return Response(
                {'id_list': list(posts)},
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return make_exception_response(e)

class PostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            user = request.user
            user_check(user)

            post_id = request.data.get('id')
            post = Posts.objects.get(id=post_id)

            return Response(
                {
                    'id': post.id,
                    'writer': post.writer,
                    'writedate': post.writedate,
                    'content': post.content
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return make_exception_response(e)
    def post(self, request):
        try:
            user = request.user
            user_check(user)

            writer = request.data.get('writer')
            writedate = request.data.get('writedate')
            content = request.data.get('content')
            id_prefix = request.data.get('id_prefix', '')

            new_id = generate_new_id(id_prefix)

            Posts.objects.create(id=new_id, writer=writer, writedate=writedate, content=content)

            return Response(
                {'id': new_id},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return make_exception_response(e)
