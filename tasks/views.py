from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from .models import Task
from .forms import TaskForm


class TaskListView(View):
    """
    View to display all tasks with filtering and sorting capabilities.
    
    GET Parameters:
    - status: Filter tasks by status (To Do, In Progress, Done)
    - sort: Sort tasks by 'priority' or 'due_date'
    """
    
    template_name = 'tasks/task_list.html'
    
    def get(self, request):
        """
        Handle GET request to display filtered and sorted tasks.
        """
        # Get all tasks
        tasks = Task.objects.all()
        
        # Get filter and sort parameters from request
        status_filter = request.GET.get('status', '')
        sort_by = request.GET.get('sort', '-created_at')
        
        # Apply status filter if provided
        if status_filter and status_filter in ['To Do', 'In Progress', 'Done']:
            tasks = tasks.filter(status=status_filter)
        
        # Apply sorting
        valid_sort_fields = [
            'priority', '-priority',
            'due_date', '-due_date',
            'created_at', '-created_at'
        ]
        if sort_by in valid_sort_fields:
            tasks = tasks.order_by(sort_by)
        else:
            tasks = tasks.order_by('-created_at')
        
        # Prepare context data
        context = {
            'tasks': tasks,
            'status_choices': Task.STATUS_CHOICES,
            'priority_choices': Task.PRIORITY_CHOICES,
            'current_status_filter': status_filter,
            'current_sort': sort_by,
        }
        
        return render(request, self.template_name, context)


# Function-based view alternative (optional)
def task_list(request):
    """
    Function-based view for task list with filtering and sorting.
    
    GET Parameters:
    - status: Filter tasks by status (To Do, In Progress, Done)
    - sort: Sort tasks by 'priority' or 'due_date'
    """
    # Get all tasks
    tasks = Task.objects.all()
    
    # Get filter and sort parameters from request
    status_filter = request.GET.get('status', '')
    sort_by = request.GET.get('sort', '-created_at')
    
    # Apply status filter if provided
    if status_filter and status_filter in ['To Do', 'In Progress', 'Done']:
        tasks = tasks.filter(status=status_filter)
    
    # Apply sorting
    valid_sort_fields = [
        'priority', '-priority',
        'due_date', '-due_date',
        'created_at', '-created_at'
    ]
    if sort_by in valid_sort_fields:
        tasks = tasks.order_by(sort_by)
    else:
        tasks = tasks.order_by('-created_at')
    
    # Prepare context data
    context = {
        'tasks': tasks,
        'status_choices': Task.STATUS_CHOICES,
        'priority_choices': Task.PRIORITY_CHOICES,
        'current_status_filter': status_filter,
        'current_sort': sort_by,
    }
    
    return render(request, 'tasks/task_list.html', context)


# Create Task View
class TaskCreateView(CreateView):
    """
    View to create a new task.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Add New Task'
        context['button_text'] = 'Create Task'
        return context


def add_task(request):
    """
    Function-based view to add a new task.
    """
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm()
    
    context = {
        'form': form,
        'title': 'Add New Task',
        'button_text': 'Create Task',
    }
    return render(request, 'tasks/task_form.html', context)


# Update Task View
class TaskUpdateView(UpdateView):
    """
    View to edit an existing task.
    """
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_form.html'
    success_url = reverse_lazy('tasks:task_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Edit Task: {self.object.title}'
        context['button_text'] = 'Update Task'
        return context


def edit_task(request, pk):
    """
    Function-based view to edit a task.
    """
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('tasks:task_list')
    else:
        form = TaskForm(instance=task)
    
    context = {
        'form': form,
        'task': task,
        'title': f'Edit Task: {task.title}',
        'button_text': 'Update Task',
    }
    return render(request, 'tasks/task_form.html', context)


# Delete Task View
class TaskDeleteView(DeleteView):
    """
    View to delete a task.
    """
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('tasks:task_list')


def delete_task(request, pk):
    """
    Function-based view to delete a task.
    """
    task = get_object_or_404(Task, pk=pk)
    
    if request.method == 'POST':
        task.delete()
        return redirect('tasks:task_list')
    
    context = {
        'task': task,
    }
    return render(request, 'tasks/task_confirm_delete.html', context)

