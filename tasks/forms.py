from django import forms
from .models import Task


class TaskForm(forms.ModelForm):
    """
    Form for creating and editing tasks.
    
    Fields:
    - title: Task title
    - description: Task description
    - due_date: Due date for the task
    - priority: Task priority level
    - status: Task status
    """
    
    due_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        help_text='Select the due date for this task'
    )
    
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 4,
            'placeholder': 'Enter task description (optional)'
        }),
        required=False,
        help_text='Provide details about the task'
    )
    
    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'priority', 'status']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter task title',
                'class': 'form-input'
            }),
            'priority': forms.RadioSelect(),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        help_texts = {
            'title': 'Give your task a clear, descriptive title',
            'priority': 'Select the priority level (1=High, 2=Medium, 3=Low)',
            'status': 'Choose the current status of the task',
        }
