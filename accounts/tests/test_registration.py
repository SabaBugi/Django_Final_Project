import pytest
from django.urls import reverse
from accounts.models import CustomUser

@pytest.mark.django_db
def test_user_registration(client):
    registration_url = reverse('accounts:register')
    data = {
        'email': 'testuser@example.com',
        'password1': 'StrongPassword123',
        'password2': 'StrongPassword123',
        'first_name': 'Test',
        'last_name': 'User'
    }
    response = client.post(registration_url, data)
    assert response.status_code == 302
    assert CustomUser.objects.filter(email='testuser@example.com').exists()