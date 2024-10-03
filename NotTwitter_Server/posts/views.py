from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Posts

class PostlistView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
            id_prefix = request.data.get('id_prefix', '')
            id_regex = f"^{id_prefix}(/[0-9]+)?$" if id_prefix else '^[0-9]+$'
            
            posts = Posts.objects.filter(id__regex=id_regex).values_list('id', flat=True)
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
                {'error': 'An error occurred while retrieving posts.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class PostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        try:
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
        except Posts.DoesNotExist:
            return Response(
                {'error': 'Post not found.'},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {'error': 'An error occurred while retrieving the post.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def post(self, request):
        try:
            writer = request.data.get('writer')
            writedate = request.data.get('writedate')
            content = request.data.get('content')
            id_prefix = request.data.get('id_prefix', '')

            new_id = self.generate_new_id(id_prefix)

            Posts.objects.create(id=new_id, writer=writer, writedate=writedate, content=content)

            return Response(
                {'id': new_id},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {'error': 'An error occurred while creating the post.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def generate_new_id(self, id_prefix):
        id_regex = f"^{id_prefix}/[0-9]+$" if id_prefix else '^[0-9]+$'
        new_id_suffix = Posts.objects.filter(id__regex=id_regex).count()

        if id_prefix:
            return f"{id_prefix}/{new_id_suffix}"
        return str(new_id_suffix)
