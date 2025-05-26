import pytest
from django.urls import reverse
from accounts.models import CustomUser
from tasks.models import Project

@pytest.mark.django_db
def test_project_creation(client):
    
    user = CustomUser.objects.create_user(
        email='projectuser@example.com',
        password='TestPassword123'
    )
    client.login(email='projectuser@example.com', password='TestPassword123')

    create_url = reverse('tasks:create_project')
    data = {
        'name': 'My Test Project',
        'description': 'This is a test project.'
    }
    response = client.post(create_url, data)
    assert response.status_code == 302  

    project = Project.objects.get(name='My Test Project')
    assert project.owner == user