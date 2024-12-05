import pytest
from django.urls import reverse

def test_user_login_successful(api_client, test_user):
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    assert response.status_code == 200
    assert 'access' in response.data
    assert 'refresh' in response.data

def test_user_login_wrong_password(api_client, test_user):
    url = reverse('token_obtain_pair')
    response = api_client.post(url, {
        'username': 'testuser',
        'password': 'wrongpass'
    })
    
    assert response.status_code == 401

def test_token_refresh(api_client, test_user):
    login_url = reverse('token_obtain_pair')
    login_response = api_client.post(login_url, {
        'username': 'testuser',
        'password': 'testpass123'
    })
    
    refresh_url = reverse('token_refresh')
    refresh_response = api_client.post(refresh_url, {
        'refresh': login_response.data['refresh']
    })
    
    assert refresh_response.status_code == 200
    assert 'access' in refresh_response.data
