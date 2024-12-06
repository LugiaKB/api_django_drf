import django_filters
from posts.models import Post

class PostFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name='user__username')

    class Meta:
        model = Post
        fields = ['username']