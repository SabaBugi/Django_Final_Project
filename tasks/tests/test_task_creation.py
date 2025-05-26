import pytest
from django.urls import reverse
from accounts.models import CustomUser
from tasks.models import Task

@pytest.mark.django_db
def test_task_creation(client):
    
    user = CustomUser.objects.create_user(
        email='taskuser@example.com',
        password='TestPassword123'
    )
    client.login(email='taskuser@example.com', password='TestPassword123')

    create_url = reverse('tasks:create_task')
    data = {
        'title': 'My Test Task',
        'description': 'This is a test task.',
        'due_date': '2030-01-01',
        'priority': 'M', 
    }
    response = client.post(create_url, data)
    assert response.status_code == 302 

    task = Task.objects.get(title='My Test Task')
    assert task.user == user