from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """
    Admin interface for Task model.
    
    Features:
    - List display: Shows title, due_date, priority, and status
    - Filters: Filter by status and priority
    - Search: Search by title and description
    - Ordering: Default ordering by -created_at
    """
    
    list_display = ('title', 'due_date', 'priority', 'status', 'created_at')
    list_filter = ('status', 'priority', 'created_at')
    search_fields = ('title', 'description')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Task Information', {
            'fields': ('title', 'description'),
        }),
        ('Task Details', {
            'fields': ('due_date', 'priority', 'status'),
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
