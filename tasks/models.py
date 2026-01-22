from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Task(models.Model):
    """
    Task model for the Task List application.
    
    Fields:
    - title: The task title
    - description: Detailed description of the task
    - due_date: When the task should be completed
    - priority: Priority level (1=High, 2=Medium, 3=Low)
    - status: Current status of the task
    - created_at: When the task was created
    - updated_at: Last time the task was modified
    """
    
    PRIORITY_CHOICES = [
        (1, 'High'),
        (2, 'Medium'),
        (3, 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('To Do', 'To Do'),
        ('In Progress', 'In Progress'),
        ('Done', 'Done'),
    ]
    
    title = models.CharField(
        max_length=200,
        help_text="Task title"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed task description"
    )
    due_date = models.DateField(
        help_text="Due date for the task"
    )
    priority = models.IntegerField(
        choices=PRIORITY_CHOICES,
        default=2,
        validators=[MinValueValidator(1), MaxValueValidator(3)],
        help_text="Priority level: 1=High, 2=Medium, 3=Low"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='To Do',
        help_text="Current status of the task"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', '-priority']),
            models.Index(fields=['due_date']),
        ]
    
    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"
    
    def get_priority_display_custom(self):
        """Return priority as string."""
        return dict(self.PRIORITY_CHOICES).get(self.priority, 'Unknown')
