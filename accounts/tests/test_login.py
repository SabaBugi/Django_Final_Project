import pytest
from django.urls import reverse
from accounts.models import CustomUser

@pytest.mark.django_db
def test_user_login(client):
    # Create a user
    user = CustomUser.objects.create_user(
        email='loginuser@example.com',
        password='TestPassword123',
        first_name='Login',
        last_name='User'
    )
    login_url = reverse('accounts:login')
    response = client.post(login_url, {
        'username': user.email, 
        'password': 'TestPassword123'
    })

    assert response.status_code == 302
   
    response = client.get(reverse('accounts:profile'))
    assert response.wsgi_request.user.is_authenticated