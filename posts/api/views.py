from rest_framework import viewsets, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from posts.models import Post
from posts.api.serializers import PostSerializer
from posts.api.filters import PostFilter

@extend_schema_view(
    list=extend_schema(
        description="Retrieve a list of posts. This endpoint is accessible to all users and can be ordered by timestamp and filtered by username."
    ),
    retrieve=extend_schema(
        description="Retrieve a specific post by ID. This endpoint is accessible to all users."
    ),
    create=extend_schema(
        description="Create a new post. This endpoint requires authentication."
    ),
    update=extend_schema(
        description="Update an existing post. This endpoint requires authentication and the user must be the owner of the post."
    ),
    partial_update=extend_schema(
        description="Partially update an existing post. This endpoint requires authentication and the user must be the owner of the post."
    ),
    destroy=extend_schema(
        description="Delete an existing post. This endpoint requires authentication and the user must be the owner of the post."
    ),
)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    filterset_class = PostFilter
    ordering_fields = ['created_at']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({'detail': 'You do not have permission to edit this post.'}, status=403)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({'detail': 'You do not have permission to edit this post.'}, status=403)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({'detail': 'You do not have permission to delete this post.'}, status=403)
        return super().destroy(request, *args, **kwargs)
