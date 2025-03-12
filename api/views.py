from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .paginators import StandardResultSetPagination

from blog.models import Post, Tag
from .serializers import PostSerializer, TagSerializer

@api_view(['GET'])
def getPost(request):
    posts = Post.objects.all()
    serializer = PostSerializer(posts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getTag(request):
    tags = Tag.objects.all()
    serializer = TagSerializer(tags, many=True)
    return Response(serializer.data)

class PostList(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = StandardResultSetPagination

class TagList(generics.ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = StandardResultSetPagination

