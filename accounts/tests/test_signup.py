import pytest
from django.urls import reverse

from django.contrib.auth import get_user_model
User = get_user_model()

@pytest.mark.django_db
def test_user_signup_successful(api_client, test_user_data):
    url = reverse('signup')
    response = api_client.post(url, test_user_data)
    
    assert response.status_code == 201
    assert 'access' in response.data
    assert 'refresh' in response.data
    
    user = User.objects.get(username=test_user_data['username'])
    assert user.email == test_user_data['email']

@pytest.mark.django_db
def test_user_signup_password_mismatch(api_client, test_user_data):
    test_user_data['password_confirmation'] = 'wrongpass'
    url = reverse('signup')
    response = api_client.post(url, test_user_data)
    
    assert response.status_code == 400
    assert 'non_field_errors' in response.data
    assert response.data['non_field_errors'][0] == 'The passwords do not match.'

def test_user_signup_duplicate_username(api_client, test_user, test_user_data):
    test_user_data['username'] = test_user.username
    url = reverse('signup')
    response = api_client.post(url, test_user_data)
    
    assert response.status_code == 400
    assert 'username' in response.data