import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.fixture
def user():
    user = User.objects.create_user(username='testuser', password='testpassword')
    return user

@pytest.fixture
def post(user):
    post = Post.objects.create(title='Test Post', content='This is a test post', user=user)
    return post

@pytest.fixture
def api_client():
    return APIClient()