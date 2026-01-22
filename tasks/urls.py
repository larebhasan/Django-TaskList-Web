from django.urls import path
from . import views

app_name = 'tasks'

urlpatterns = [
    # List and view tasks
    path('', views.task_list, name='task_list'),
    
    # Create task
    path('add/', views.add_task, name='add_task'),
    
    # Edit task
    path('<int:pk>/edit/', views.edit_task, name='edit_task'),
    
    # Delete task
    path('<int:pk>/delete/', views.delete_task, name='delete_task'),
]
