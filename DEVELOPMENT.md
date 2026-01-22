# Development Guide

## Setting Up Development Environment

### 1. Initial Setup

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install dependencies
pip install django

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 2. Running the Development Server

```bash
python manage.py runserver
```

Access the application at:
- Task List: http://127.0.0.1:8000/tasks/
- Admin Panel: http://127.0.0.1:8000/admin/

## Project Architecture

### Models (`tasks/models.py`)

The `Task` model is the core of the application with the following key features:

- **Field Validation**: Uses Django validators to ensure data integrity
- **Model Meta**: Includes ordering and database indexes for performance
- **Custom Methods**: `get_priority_display_custom()` for priority display
- **String Representation**: Meaningful `__str__()` method for admin interface

### Views (`tasks/views.py`)

Two implementations provided:

1. **Class-based View** (`TaskListView`): Object-oriented approach
2. **Function-based View** (`task_list`): Procedural approach

Both implement:
- Status filtering with validation
- Multiple sorting options
- Safe parameter handling

### Templates (`tasks/templates/tasks/task_list.html`)

Features:
- Responsive CSS with mobile breakpoints
- Interactive filter/sort controls with form
- Color-coded status and priority badges
- Overdue task highlighting
- Empty state messaging

### Tests (`tasks/tests.py`)

Comprehensive test suite with 23 tests:

**Test Classes**:
1. `TaskModelTestCase`: Model functionality (5 tests)
2. `TaskListViewTestCase`: View logic and filtering/sorting (18 tests)

**Key Test Patterns**:
- Setup data with `setUp()` method
- Using `Client()` for view testing
- QuerySet assertion methods
- Context data validation
- Edge case handling

## Code Quality Guidelines

### Style

- Follow PEP 8 naming conventions
- Use meaningful variable names
- Add docstrings to classes and functions
- Use type hints where helpful (Python 3.8+)

### Comments

Add comments for:
- Non-obvious logic
- Complex algorithms
- Important business rules
- Tricky edge cases

Avoid:
- Over-commenting obvious code
- Comments that duplicate the code

### Testing

- Write tests for new features
- Aim for >80% code coverage
- Test edge cases and error conditions
- Use descriptive test names

## Common Development Tasks

### Adding a New Filter

1. Update the view to handle the new parameter
2. Add validation for the new filter
3. Update the template with UI control
4. Write tests for the new filter

Example in `views.py`:

```python
# Get new filter parameter
new_filter = request.GET.get('new_filter', '')

# Apply filter if valid
if new_filter in valid_options:
    tasks = tasks.filter(new_field=new_filter)

# Add to context
context['new_filter'] = new_filter
```

### Adding a New Task Field

1. Add field to `Task` model in `models.py`
2. Create migration: `python manage.py makemigrations`
3. Run migration: `python manage.py migrate`
4. Update template if needed
5. Add admin configuration
6. Write tests

Example in `models.py`:

```python
assignee = models.ForeignKey(
    User,
    on_delete=models.SET_NULL,
    null=True,
    blank=True
)
```

### Running Tests

```bash
# Run all tests
python manage.py test tasks

# Run with coverage
pip install coverage
coverage run --source='tasks' manage.py test tasks
coverage report

# Run specific test class
python manage.py test tasks.tests.TaskListViewTestCase

# Run specific test method
python manage.py test tasks.tests.TaskListViewTestCase.test_filter_by_status_todo
```

## Database Management

### Creating Migrations

```bash
python manage.py makemigrations
python manage.py makemigrations --name descriptive_name
```

### Applying Migrations

```bash
python manage.py migrate
python manage.py migrate tasks
python manage.py migrate tasks 0001_initial
```

### Checking Migration Status

```bash
python manage.py showmigrations
```

### Reverting Migrations

```bash
python manage.py migrate tasks 0001_initial
```

### Dumping Data

```bash
python manage.py dumpdata tasks > fixtures/tasks.json
```

### Loading Fixtures

```bash
python manage.py loaddata fixtures/tasks.json
```

## Debugging

### Using Django Debug Toolbar

```bash
pip install django-debug-toolbar
```

Add to `INSTALLED_APPS` in settings:
```python
INSTALLED_APPS += ['debug_toolbar']
```

Add to URLs:
```python
if DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]
```

### Using Django Shell

```bash
python manage.py shell

# In shell:
from tasks.models import Task
tasks = Task.objects.filter(priority=1)
for task in tasks:
    print(task)
```

### Logging

Enable logging in settings for debugging:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG',
    },
}
```

## Performance Optimization

### Database Queries

- Use `select_related()` for ForeignKey
- Use `prefetch_related()` for reverse relations
- Use `only()` and `defer()` for field selection
- Add database indexes (already done in Task model)

Example:

```python
# Optimized query
tasks = Task.objects.select_related('assignee').only(
    'title', 'due_date', 'priority'
)
```

### Caching

Add to views:

```python
from django.views.decorators.cache import cache_page

@cache_page(60 * 5)  # Cache for 5 minutes
def task_list(request):
    ...
```

## Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in settings
- [ ] Update `ALLOWED_HOSTS`
- [ ] Use environment variables for `SECRET_KEY`
- [ ] Set up proper database (PostgreSQL, MySQL)
- [ ] Configure HTTPS
- [ ] Set up static files collection
- [ ] Configure email backend
- [ ] Set up logging and monitoring
- [ ] Run security checks: `python manage.py check --deploy`

## Useful Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Two Scoops of Django](https://www.feldroy.com/books/two-scoops-of-django-3-x/)
- [Real Python - Django Tutorials](https://realpython.com/search?q=django)
- [Django REST Framework](https://www.django-rest-framework.org/)

## Troubleshooting Common Issues

### ImportError for models

Solution: Ensure `INSTALLED_APPS` includes the app.

### Migration conflicts

Solution: 
```bash
python manage.py migrate --fake
python manage.py makemigrations
python manage.py migrate
```

### Static files not loading

Solution:
```bash
python manage.py collectstatic
```

### Database locked error

Solution: Delete `db.sqlite3` and re-migrate (development only).
