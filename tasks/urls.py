from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # Home Page
    path('', views.home, name='home'),

    # Task Management
    path('task_list/', views.task_list, name='task_list'),
    path('tasks/create/', views.create_task, name='create_task'),
    path('tasks/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'), # No HTMX partial logic in view

    # Task Tags (current view always redirects, might need separate partial if you want in-place updates)
    path('tasks/<int:pk>/tags/', views.task_tags_add, name='add_tag'),
    path('tags/<int:tag_id>/', views.tasks_by_tag, name='tasks_by_tag'), # No HTMX partial logic in view

    # Project Management
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:pk>/', views.project_detail, name='project_detail'), # No HTMX partial logic in view
    path('projects/<int:pk>/edit/', views.edit_project, name='edit_project'),
    path('projects/<int:pk>/delete/', views.delete_project, name='delete_project'),

    # Comments (current view always redirects, might need separate partial if you want in-place updates)
    path('comments/<int:task_id>/add/', views.add_comment, name='add_comment'),
]
