import pytest
from django.urls import reverse
from rest_framework import status
from posts.models import Post
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_list_posts(api_client, post):
    url = reverse('post-list')
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

@pytest.mark.django_db
def test_list_posts_filtered_by_author(api_client, post, user):
    url = reverse('post-list') + f'?user={user.id}'
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1

@pytest.mark.django_db
def test_create_post(api_client, user):
    api_client.force_authenticate(user=user)
    url = reverse('post-list')
    data = {'title': 'New Post', 'content': 'Content of the new post'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Post.objects.count() == 1
    assert Post.objects.get().title == 'New Post'

@pytest.mark.django_db
def test_create_post_unauthenticated(api_client):
    url = reverse('post-list')
    data = {'title': 'New Post', 'content': 'Content of the new post'}
    response = api_client.post(url, data, format='json')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_update_post(api_client, user, post):
    api_client.force_authenticate(user=user)
    url = reverse('post-detail', args=[post.id])
    data = {'title': 'Updated Title', 'content': 'Updated content'}
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    post.refresh_from_db()
    assert post.title == 'Updated Title'

@pytest.mark.django_db
def test_update_post_not_author(api_client, post):
    other_user = User.objects.create_user(username='otheruser', password='password')
    api_client.force_authenticate(user=other_user)
    url = reverse('post-detail', args=[post.id])
    data = {'title': 'Updated Title', 'content': 'Updated content'}
    response = api_client.patch(url, data, format='json')
    assert response.status_code == status.HTTP_403_FORBIDDEN

@pytest.mark.django_db
def test_delete_post(api_client, user, post):
    api_client.force_authenticate(user=user)
    url = reverse('post-detail', args=[post.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Post.objects.count() == 0

@pytest.mark.django_db
def test_delete_post_not_author(api_client, post):
    other_user = User.objects.create_user(username='otheruser', password='password')
    api_client.force_authenticate(user=other_user)
    url = reverse('post-detail', args=[post.id])
    response = api_client.delete(url)
    assert response.status_code == status.HTTP_403_FORBIDDEN
