# Testing Documentation

## Overview

This Django Task List application includes a comprehensive test suite with **23 passing tests** covering:
- Task model functionality
- View logic with filtering and sorting
- Context data validation
- Edge cases and error handling

All tests can be run with: `python manage.py test tasks`

## Test Structure

### TaskModelTestCase (5 tests)

Tests for the Task model in `tasks.models.Task`.

#### test_task_creation
- **Purpose**: Verify that tasks are created with correct initial values
- **Scenario**: Create a task and check its attributes
- **Assertion**: Title, priority, and status match expected values

#### test_task_string_representation
- **Purpose**: Verify the `__str__()` method returns meaningful text
- **Scenario**: Convert task to string
- **Assertion**: String contains title and status display

#### test_priority_choices
- **Purpose**: Verify priority choice display method works correctly
- **Scenario**: Create tasks with different priorities
- **Assertion**: `get_priority_display_custom()` returns 'High', 'Medium', or 'Low'

#### test_status_choices
- **Purpose**: Verify status choice display method works correctly
- **Scenario**: Create tasks with different statuses
- **Assertion**: `get_status_display()` returns 'To Do', 'In Progress', or 'Done'

#### test_task_update
- **Purpose**: Verify that tasks can be modified and saved
- **Scenario**: Create a task, change its status, save it
- **Assertion**: Task status changes persist in database

### TaskListViewTestCase (18 tests)

Tests for the task_list view in `tasks.views.task_list`.

#### View Rendering Tests (4 tests)

##### test_task_list_view_returns_200
- **Purpose**: Verify the view is accessible
- **HTTP Status**: 200 OK
- **URL**: `/tasks/`

##### test_task_list_view_uses_correct_template
- **Purpose**: Verify correct template is rendered
- **Expected Template**: `tasks/task_list.html`

##### test_task_list_view_context
- **Purpose**: Verify all required context variables are provided
- **Expected Variables**:
  - `tasks`: QuerySet of tasks
  - `status_choices`: Status options
  - `priority_choices`: Priority options
  - `current_status_filter`: Current filter value
  - `current_sort`: Current sort field

##### test_all_tasks_displayed_by_default
- **Purpose**: Verify all tasks shown without filters
- **Setup**: Create 4 tasks
- **Expected**: All 4 tasks in context

#### Filtering Tests (4 tests)

##### test_filter_by_status_todo
- **Purpose**: Filter tasks with 'To Do' status
- **Query Parameter**: `?status=To%20Do`
- **Expected**: Only 'To Do' tasks returned

##### test_filter_by_status_in_progress
- **Purpose**: Filter tasks with 'In Progress' status
- **Query Parameter**: `?status=In%20Progress`
- **Expected**: Only 'In Progress' tasks returned

##### test_filter_by_status_done
- **Purpose**: Filter tasks with 'Done' status
- **Query Parameter**: `?status=Done`
- **Expected**: Only 'Done' tasks returned

##### test_filter_by_invalid_status
- **Purpose**: Verify invalid status shows all tasks
- **Query Parameter**: `?status=Invalid%20Status`
- **Expected**: All tasks returned (filter ignored)

#### Sorting Tests (6 tests)

##### test_sort_by_priority_ascending
- **Purpose**: Sort by priority Low to High (1, 1, 2, 3)
- **Query Parameter**: `?sort=priority`
- **Verification**: Priority sequence is ascending

##### test_sort_by_priority_descending
- **Purpose**: Sort by priority High to Low (3, 2, 1, 1)
- **Query Parameter**: `?sort=-priority`
- **Verification**: Priority sequence is descending

##### test_sort_by_due_date_ascending
- **Purpose**: Sort by due date earliest first
- **Query Parameter**: `?sort=due_date`
- **Verification**: Due dates in ascending order

##### test_sort_by_due_date_descending
- **Purpose**: Sort by due date latest first
- **Query Parameter**: `?sort=-due_date`
- **Verification**: Due dates in descending order

##### test_sort_by_created_at_descending
- **Purpose**: Sort by creation date newest first
- **Query Parameter**: `?sort=-created_at`
- **Verification**: Most recent task appears first

##### test_sort_by_invalid_field
- **Purpose**: Invalid sort defaults to -created_at
- **Query Parameter**: `?sort=invalid_field`
- **Verification**: Uses default ordering (-created_at)

#### Combined Filter and Sort Tests (2 tests)

##### test_filter_and_sort_combined
- **Purpose**: Apply both status filter and priority sort
- **Query Parameters**: `?status=To%20Do&sort=priority`
- **Verification**:
  - Only 'To Do' tasks returned
  - Results sorted by priority
  - Count equals number of 'To Do' tasks

##### test_filter_and_sort_with_due_date
- **Purpose**: Apply status filter and due date sort
- **Query Parameters**: `?status=To%20Do&sort=due_date`
- **Verification**:
  - Only 'To Do' tasks returned
  - Results sorted by due date
  - Due dates in ascending order

#### Context Tests (2 tests)

##### test_current_filter_in_context
- **Purpose**: Verify current filter value passed to template
- **Query Parameter**: `?status=Done`
- **Verification**: `context['current_status_filter'] == 'Done'`

##### test_current_sort_in_context
- **Purpose**: Verify current sort value passed to template
- **Query Parameter**: `?sort=priority`
- **Verification**: `context['current_sort'] == 'priority'`

## Running Tests

### Run All Tests

```bash
python manage.py test tasks
```

Output:
```
Ran 23 tests in 0.113s
OK
```

### Run With Verbose Output

```bash
python manage.py test tasks -v 2
```

Shows each test name and result.

### Run Specific Test Class

```bash
# Model tests only
python manage.py test tasks.tests.TaskModelTestCase

# View tests only
python manage.py test tasks.tests.TaskListViewTestCase
```

### Run Specific Test Method

```bash
python manage.py test tasks.tests.TaskListViewTestCase.test_filter_by_status_todo
```

### Run With Test Runner Options

```bash
# Fail on first error
python manage.py test tasks -f

# Keep test database
python manage.py test tasks --keepdb

# Show slowest tests
python manage.py test tasks -v 2 --slowest 5
```

## Test Coverage Analysis

### Model Tests: 5/5 (100%)
- Model creation: ✓
- String representation: ✓
- Choice fields: ✓
- Data persistence: ✓
- Field validation: ✓ (implicit via creation)

### View Tests: 18/18 (100%)
- HTTP response: ✓
- Template rendering: ✓
- Context variables: ✓
- Default behavior: ✓
- Status filtering (4 scenarios): ✓
- Priority sorting (2 scenarios): ✓
- Date sorting (2 scenarios): ✓
- Creation date sorting: ✓
- Invalid parameters: ✓
- Combined filtering/sorting (2 scenarios): ✓
- Context state (2 checks): ✓

### Total Coverage: 23/23 (100%)

## Test Data Setup

Each test class uses `setUp()` to create sample data:

### TaskModelTestCase Setup
Creates 3 tasks with different priorities and statuses:
```python
task1: High priority, To Do
task2: Medium priority, In Progress
task3: Low priority, Done
```

### TaskListViewTestCase Setup
Creates 4 tasks for filtering/sorting:
```python
task1: To Do, High priority, due in 1 day
task2: In Progress, Medium priority, due in 5 days
task3: Done, Low priority, due in 10 days
task4: To Do, High priority, due in 3 days
```

## Edge Cases and Error Handling

The tests verify:

1. **Invalid Filters**: Invalid status values are ignored, all tasks returned
2. **Invalid Sorts**: Unknown sort fields default to '-created_at'
3. **Empty QuerySets**: Correctly handles filtering that returns no results
4. **Multiple Results**: Correctly orders tasks when multiple match criteria
5. **Type Safety**: Uses correct assertion methods for different types

## Continuous Integration

To set up automated testing:

### GitHub Actions Example

Create `.github/workflows/tests.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: 3.9
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    - name: Run tests
      run: |
        python manage.py test tasks
```

## Debugging Failed Tests

### Verbose Output
```bash
python manage.py test tasks -v 2
```

### Failure Details
```bash
python manage.py test tasks --verbosity=3
```

### Using Django Shell for Debugging
```bash
python manage.py shell
>>> from tasks.models import Task
>>> Task.objects.all().count()
```

### Adding Print Statements
Add debugging in test:
```python
def test_example(self):
    tasks = Task.objects.all()
    print(f"Found {tasks.count()} tasks")
    self.assertEqual(tasks.count(), 4)
```

Run with stdout:
```bash
python manage.py test tasks --noinput --keepdb --verbosity 2 --pdb
```

## Best Practices Applied

1. **Test Isolation**: Each test is independent and creates its own data
2. **Clear Naming**: Test names describe what is being tested
3. **Single Assertion**: Tests focus on one thing (generally)
4. **DRY**: Shared setup code in `setUp()` method
5. **Descriptive Messages**: Docstrings explain test purpose
6. **Edge Cases**: Tests cover both happy path and error conditions
7. **Performance**: Tests complete in <150ms total

## Extending Tests

### Adding New Tests

Pattern:
```python
def test_new_feature(self):
    """Test description."""
    # Setup
    # Execute
    # Assert
    pass
```

Example:
```python
def test_filter_by_new_field(self):
    """Test filtering tasks by new_field."""
    # Setup
    response = self.client.get(self.url, {'new_field': 'value'})
    
    # Execute
    tasks = response.context['tasks']
    
    # Assert
    self.assertEqual(tasks.count(), 1)
    self.assertEqual(tasks[0].new_field, 'value')
```

### Test Coverage Tool

Install and use coverage:
```bash
pip install coverage

# Run tests with coverage
coverage run --source='tasks' manage.py test tasks

# Generate report
coverage report

# Generate HTML report
coverage html
```

## Troubleshooting Test Issues

### Database Locked Error
```bash
# Clear test database
rm db.sqlite3
python manage.py migrate
```

### Import Errors
- Ensure app is in `INSTALLED_APPS`
- Check Python path

### Assertion Errors
- Add print statements for debugging
- Use `-v 2` for verbose output
- Check test data setup in `setUp()`

### Timing Issues
- Tests should be fast (<1s total)
- Avoid external API calls
- Use mocking for external dependencies
