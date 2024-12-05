import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'codeleap_network.settings.local')
django.setup()

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123'
    )
    return user

@pytest.fixture
def test_user_data():
    return {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'newpass123',
        'password_confirmation': 'newpass123'
    }