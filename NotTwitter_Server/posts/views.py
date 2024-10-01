from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import Posts

# Create your views here.
class PostlistView(APIView):
    def get(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise AuthenticationFailed('Authentication credentials were not provided.')

            id_prefix = request.data.get('id_prefix')
            if id_prefix == '':
                id = '^[0-9]+$'
            else:
                id = '^' + id_prefix + '(/[0-9]+)?$'
            
            posts = Posts.objects.filter(id__regex=id).values_list('id', flat=True)

            return Response(
                {'id_list': list(posts)},
                status=status.HTTP_200_OK
            )
        except Posts.DoesNotExist:
            return Response(
                {'error': 'No posts found with the given prefix.'}, 
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostView(APIView):
    def get(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise AuthenticationFailed('Authentication credentials were not provided.')

            id = request.data.get('id')
            
            result = Posts.objects.filter(id=id).get()
            return Response(
                {
                    'id': result.id,
                    'writer': result.writer,
                    'writedate': result.writedate,
                    'content': result.content
                },
                status=status.HTTP_200_OK
            )
        except Posts.DoesNotExist:
            return Response(
                {'error': 'Post not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def post(self, request):
        try:
            user = request.user
            if user.is_anonymous:
                raise AuthenticationFailed('Authentication credentials were not provided.')

            id_prefix = request.data.get('id_prefix')
            writer = request.data.get('writer')
            writedate = request.data.get('writedate')
            content = request.data.get('content')

            if id_prefix == '':
                id = '^' + '[0-9]+$'
            else:
                id = '^' + id_prefix + '/[0-9]+$'
            print('id is', id)
            
            new_id = Posts.objects.filter(id__regex=id).count()
            if id_prefix == '':
                new_id = str(new_id)
            else:
                new_id = id_prefix + '/' + str(new_id)
            print('new id is', new_id)

            Posts.objects.create(id=new_id, writer=writer, writedate=writedate, content=content)
            return Response(
                {'id': new_id},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
