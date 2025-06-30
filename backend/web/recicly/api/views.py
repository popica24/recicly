from typing import Optional
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404

from .serializers import BlogPostSerializer
from .models import BlogPost


class PostsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class PostsView(APIView):
    def get(self, request: Request, pk: Optional[int] = None) -> Response:
        if pk:
            post: BlogPost = get_object_or_404(BlogPost, pk=pk)
            serializer: BlogPostSerializer = BlogPostSerializer(post)
            return Response(serializer.data)
        else:
            posts = BlogPost.objects.all()
            paginator = PostsPagination()
            paginated_posts = paginator.paginate_queryset(posts, request)
            serializer: BlogPostSerializer = BlogPostSerializer(paginated_posts, many=True)
            return paginator.get_paginated_response(serializer.data)