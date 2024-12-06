from rest_framework import serializers

from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)  
    created_datetime = serializers.DateTimeField(source='created_at', read_only=True) 

    class Meta:
        model = Post
        fields = ['id', 'username', 'created_datetime', 'title', 'content']