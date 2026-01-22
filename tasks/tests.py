from django.test import TestCase, Client
from django.urls import reverse
from datetime import date, timedelta
from .models import Task


class TaskModelTestCase(TestCase):
    """Test cases for Task model."""
    
    def setUp(self):
        """Create test data."""
        self.task1 = Task.objects.create(
            title="High Priority Task",
            description="This is a high priority task",
            due_date=date.today() + timedelta(days=1),
            priority=1,
            status='To Do'
        )
        
        self.task2 = Task.objects.create(
            title="Medium Priority Task",
            description="This is a medium priority task",
            due_date=date.today() + timedelta(days=5),
            priority=2,
            status='In Progress'
        )
        
        self.task3 = Task.objects.create(
            title="Low Priority Task",
            description="This is a low priority task",
            due_date=date.today() + timedelta(days=10),
            priority=3,
            status='Done'
        )
    
    def test_task_creation(self):
        """Test that a task is created correctly."""
        self.assertEqual(self.task1.title, "High Priority Task")
        self.assertEqual(self.task1.priority, 1)
        self.assertEqual(self.task1.status, 'To Do')
    
    def test_task_string_representation(self):
        """Test the __str__ method of Task."""
        expected_str = f"{self.task1.title} ({self.task1.get_status_display()})"
        self.assertEqual(str(self.task1), expected_str)
    
    def test_priority_choices(self):
        """Test that priority choices are correctly defined."""
        self.assertEqual(self.task1.get_priority_display_custom(), 'High')
        self.assertEqual(self.task2.get_priority_display_custom(), 'Medium')
        self.assertEqual(self.task3.get_priority_display_custom(), 'Low')
    
    def test_status_choices(self):
        """Test that status choices are correctly defined."""
        self.assertEqual(self.task1.get_status_display(), 'To Do')
        self.assertEqual(self.task2.get_status_display(), 'In Progress')
        self.assertEqual(self.task3.get_status_display(), 'Done')
    
    def test_task_update(self):
        """Test that a task can be updated."""
        self.task1.status = 'In Progress'
        self.task1.save()
        
        updated_task = Task.objects.get(pk=self.task1.pk)
        self.assertEqual(updated_task.status, 'In Progress')


class TaskListViewTestCase(TestCase):
    """Test cases for task_list view."""
    
    def setUp(self):
        """Create test data and client."""
        self.client = Client()
        self.url = reverse('tasks:task_list')
        
        # Create tasks with different statuses and priorities
        self.task1 = Task.objects.create(
            title="Task 1 - To Do",
            description="First task",
            due_date=date.today() + timedelta(days=1),
            priority=1,
            status='To Do'
        )
        
        self.task2 = Task.objects.create(
            title="Task 2 - In Progress",
            description="Second task",
            due_date=date.today() + timedelta(days=5),
            priority=2,
            status='In Progress'
        )
        
        self.task3 = Task.objects.create(
            title="Task 3 - Done",
            description="Third task",
            due_date=date.today() + timedelta(days=10),
            priority=3,
            status='Done'
        )
        
        self.task4 = Task.objects.create(
            title="Task 4 - To Do",
            description="Fourth task",
            due_date=date.today() + timedelta(days=3),
            priority=1,
            status='To Do'
        )
    
    def test_task_list_view_returns_200(self):
        """Test that task_list view returns 200 status code."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
    
    def test_task_list_view_uses_correct_template(self):
        """Test that task_list view uses the correct template."""
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'tasks/task_list.html')
    
    def test_task_list_view_context(self):
        """Test that task_list view provides correct context."""
        response = self.client.get(self.url)
        
        self.assertIn('tasks', response.context)
        self.assertIn('status_choices', response.context)
        self.assertIn('priority_choices', response.context)
        self.assertIn('current_status_filter', response.context)
        self.assertIn('current_sort', response.context)
    
    def test_all_tasks_displayed_by_default(self):
        """Test that all tasks are displayed by default."""
        response = self.client.get(self.url)
        tasks = response.context['tasks']
        
        self.assertEqual(tasks.count(), 4)
    
    # Filter Tests
    def test_filter_by_status_todo(self):
        """Test filtering tasks by 'To Do' status."""
        response = self.client.get(self.url, {'status': 'To Do'})
        tasks = response.context['tasks']
        
        self.assertEqual(tasks.count(), 2)
        for task in tasks:
            self.assertEqual(task.status, 'To Do')
    
    def test_filter_by_status_in_progress(self):
        """Test filtering tasks by 'In Progress' status."""
        response = self.client.get(self.url, {'status': 'In Progress'})
        tasks = response.context['tasks']
        
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(tasks[0].title, "Task 2 - In Progress")
    
    def test_filter_by_status_done(self):
        """Test filtering tasks by 'Done' status."""
        response = self.client.get(self.url, {'status': 'Done'})
        tasks = response.context['tasks']
        
        self.assertEqual(tasks.count(), 1)
        self.assertEqual(tasks[0].title, "Task 3 - Done")
    
    def test_filter_by_invalid_status(self):
        """Test that invalid status filter shows all tasks."""
        response = self.client.get(self.url, {'status': 'Invalid Status'})
        tasks = response.context['tasks']
        
        # Should return all tasks since status is invalid
        self.assertEqual(tasks.count(), 4)
    
    # Sort Tests
    def test_sort_by_priority_ascending(self):
        """Test sorting tasks by priority (Low to High)."""
        response = self.client.get(self.url, {'sort': 'priority'})
        tasks = list(response.context['tasks'])
        
        # Should be sorted: 1 (High), 1 (High), 2 (Medium), 3 (Low)
        self.assertEqual(tasks[0].priority, 1)
        self.assertEqual(tasks[1].priority, 1)
        self.assertEqual(tasks[2].priority, 2)
        self.assertEqual(tasks[3].priority, 3)
    
    def test_sort_by_priority_descending(self):
        """Test sorting tasks by priority (High to Low)."""
        response = self.client.get(self.url, {'sort': '-priority'})
        tasks = list(response.context['tasks'])
        
        # Should be sorted: 3 (Low), 2 (Medium), 1 (High), 1 (High)
        self.assertEqual(tasks[0].priority, 3)
        self.assertEqual(tasks[1].priority, 2)
        self.assertEqual(tasks[2].priority, 1)
        self.assertEqual(tasks[3].priority, 1)
    
    def test_sort_by_due_date_ascending(self):
        """Test sorting tasks by due date (Earliest first)."""
        response = self.client.get(self.url, {'sort': 'due_date'})
        tasks = list(response.context['tasks'])
        
        # Verify order by due_date
        for i in range(len(tasks) - 1):
            self.assertLessEqual(tasks[i].due_date, tasks[i + 1].due_date)
    
    def test_sort_by_due_date_descending(self):
        """Test sorting tasks by due date (Latest first)."""
        response = self.client.get(self.url, {'sort': '-due_date'})
        tasks = list(response.context['tasks'])
        
        # Verify order by due_date (reversed)
        for i in range(len(tasks) - 1):
            self.assertGreaterEqual(tasks[i].due_date, tasks[i + 1].due_date)
    
    def test_sort_by_created_at_descending(self):
        """Test sorting tasks by created_at descending (newest first)."""
        response = self.client.get(self.url, {'sort': '-created_at'})
        tasks = list(response.context['tasks'])
        
        # task4 should be first (most recently created)
        self.assertEqual(tasks[0].pk, self.task4.pk)
    
    def test_sort_by_invalid_field(self):
        """Test that invalid sort field defaults to created_at descending."""
        response = self.client.get(self.url, {'sort': 'invalid_field'})
        tasks = list(response.context['tasks'])
        
        # Should default to -created_at ordering
        self.assertEqual(tasks[0].pk, self.task4.pk)
    
    # Combined Filter and Sort Tests
    def test_filter_and_sort_combined(self):
        """Test filtering and sorting together."""
        response = self.client.get(self.url, {
            'status': 'To Do',
            'sort': 'priority'
        })
        tasks = list(response.context['tasks'])
        
        # Should have 2 To Do tasks
        self.assertEqual(len(tasks), 2)
        
        # Both should be status 'To Do'
        for task in tasks:
            self.assertEqual(task.status, 'To Do')
        
        # Should be sorted by priority (both have priority 1)
        self.assertEqual(tasks[0].priority, 1)
        self.assertEqual(tasks[1].priority, 1)
    
    def test_filter_and_sort_with_due_date(self):
        """Test filtering by status and sorting by due date."""
        response = self.client.get(self.url, {
            'status': 'To Do',
            'sort': 'due_date'
        })
        tasks = list(response.context['tasks'])
        
        # Should have 2 To Do tasks
        self.assertEqual(len(tasks), 2)
        
        # Should be sorted by due_date
        for i in range(len(tasks) - 1):
            self.assertLessEqual(tasks[i].due_date, tasks[i + 1].due_date)
    
    def test_current_filter_in_context(self):
        """Test that current filter is passed to context."""
        response = self.client.get(self.url, {'status': 'Done'})
        
        self.assertEqual(response.context['current_status_filter'], 'Done')
    
    def test_current_sort_in_context(self):
        """Test that current sort is passed to context."""
        response = self.client.get(self.url, {'sort': 'priority'})
        
        self.assertEqual(response.context['current_sort'], 'priority')
