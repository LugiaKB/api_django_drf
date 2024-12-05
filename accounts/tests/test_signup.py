import pytest
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()


def test_user_signup_successful(api_client, test_user_data):
    url = reverse('signup')
    response = api_client.post(url, test_user_data)
    
    assert response.status_code == 201
    assert 'access' in response.data
    assert 'refresh' in response.data
    
    user = User.objects.get(username=test_user_data['username'])
    assert user.email == test_user_data['email']

def test_user_signup_password_mismatch(api_client, test_user_data):
    test_user_data['password_confirmation'] = 'wrongpass'
    url = reverse('signup')
    response = api_client.post(url, test_user_data)
    
    assert response.status_code == 400
    assert 'password' in response.data

def test_user_signup_duplicate_username(api_client, test_user, test_user_data):
    test_user_data['username'] = test_user.username
    url = reverse('signup')
    response = api_client.post(url, test_user_data)
    
    assert response.status_code == 400
    assert 'username' in response.data