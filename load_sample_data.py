"""
Script to populate the database with sample tasks.

Usage:
    python manage.py shell < load_sample_data.py

Or from Django shell:
    python manage.py shell
    >>> exec(open('load_sample_data.py').read())
"""

from datetime import date, timedelta
from tasks.models import Task

# Clear existing tasks (optional)
print("Loading sample tasks...")

# Create sample tasks
tasks_data = [
    {
        'title': 'Design system architecture',
        'description': 'Create a scalable architecture for the new system',
        'due_date': date.today() + timedelta(days=2),
        'priority': 1,  # High
        'status': 'In Progress',
    },
    {
        'title': 'Implement authentication',
        'description': 'Add user authentication with JWT tokens',
        'due_date': date.today() + timedelta(days=5),
        'priority': 1,  # High
        'status': 'To Do',
    },
    {
        'title': 'Write database schema',
        'description': 'Design and implement the database schema',
        'due_date': date.today() + timedelta(days=1),
        'priority': 2,  # Medium
        'status': 'In Progress',
    },
    {
        'title': 'Create API documentation',
        'description': 'Write comprehensive API documentation using Swagger',
        'due_date': date.today() + timedelta(days=10),
        'priority': 2,  # Medium
        'status': 'To Do',
    },
    {
        'title': 'Set up CI/CD pipeline',
        'description': 'Configure GitHub Actions for automated testing and deployment',
        'due_date': date.today() + timedelta(days=7),
        'priority': 2,  # Medium
        'status': 'To Do',
    },
    {
        'title': 'Develop user interface',
        'description': 'Build React components for the main dashboard',
        'due_date': date.today() + timedelta(days=14),
        'priority': 2,  # Medium
        'status': 'To Do',
    },
    {
        'title': 'Write unit tests',
        'description': 'Write comprehensive unit tests for all modules',
        'due_date': date.today() + timedelta(days=8),
        'priority': 2,  # Medium
        'status': 'In Progress',
    },
    {
        'title': 'Code review guidelines',
        'description': 'Create code review standards and best practices document',
        'due_date': date.today() + timedelta(days=3),
        'priority': 3,  # Low
        'status': 'To Do',
    },
    {
        'title': 'Update project documentation',
        'description': 'Update README and installation guides',
        'due_date': date.today() + timedelta(days=5),
        'priority': 3,  # Low
        'status': 'Done',
    },
    {
        'title': 'Performance optimization',
        'description': 'Optimize database queries and cache implementation',
        'due_date': date.today() + timedelta(days=21),
        'priority': 3,  # Low
        'status': 'To Do',
    },
    {
        'title': 'Setup monitoring and logging',
        'description': 'Implement ELK stack for application monitoring',
        'due_date': date.today() + timedelta(days=15),
        'priority': 2,  # Medium
        'status': 'To Do',
    },
    {
        'title': 'Client feedback meeting',
        'description': 'Schedule and conduct meeting with client for feedback',
        'due_date': date.today() + timedelta(days=4),
        'priority': 1,  # High
        'status': 'To Do',
    },
]

# Create tasks in database
created_tasks = []
for task_data in tasks_data:
    task = Task.objects.create(**task_data)
    created_tasks.append(task)
    print(f"✓ Created: {task.title}")

print(f"\nSuccessfully created {len(created_tasks)} tasks!")
print("\nSample statistics:")
print(f"  To Do: {Task.objects.filter(status='To Do').count()}")
print(f"  In Progress: {Task.objects.filter(status='In Progress').count()}")
print(f"  Done: {Task.objects.filter(status='Done').count()}")
print(f"  High Priority: {Task.objects.filter(priority=1).count()}")
print(f"  Medium Priority: {Task.objects.filter(priority=2).count()}")
print(f"  Low Priority: {Task.objects.filter(priority=3).count()}")
