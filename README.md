# Incodeks Task Sync – Coding Challenge

A Django REST API service for synchronizing tasks from an external system with enhanced reliability and user interface.

## Setup and Run Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/fjjollaa/incodeks-task-sync-django-challenge.git
cd incodeks-task-sync-django-challenge/incodeks-task-sync-django-challenge
# Note: Double directory due to repo structure - outer folder is repo root, inner contains Django project

# Create virtual environment
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run database migrations
python manage.py migrate

# Start the development server
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the dashboard.

### Running Tests
```bash
python manage.py test
```

### Docker Setup (Optional)

For containerized deployment:

```bash
# Build and start the stack
docker-compose up --build

# Run migrations
docker-compose exec web python manage.py migrate

# Run tests
docker-compose exec web python manage.py test

# Stop the stack
docker-compose down
```

### Additional Commands
- **Running migrations**: `python manage.py migrate`
- **Running tests**: `python manage.py test`

## API Endpoints

- `POST /api/sync/` - Trigger manual sync
- `GET /api/tasks/` - List tasks (supports `?status=` and `?search=` filters)
- `GET /api/sync/status/` - Get last sync status
- `DELETE /api/tasks/<id>/` - Delete a task

## Part 1 - Code Review and Improvements

### Issues Identified and Fixed

1. **Duplicate Records Issue**
   - **Problem**: Tasks could be duplicated on each sync run since `external_id` had no unique constraint
   - **Fix**: Added `unique=True` to `external_id` field in Task model
   - **Impact**: Prevents duplicate tasks with same external ID

2. **Non-Idempotent Sync**
   - **Problem**: Sync always created new tasks instead of updating existing ones
   - **Fix**: Replaced `Task.objects.create()` with `Task.objects.update_or_create()`
   - **Impact**: Sync is now idempotent - safe to run multiple times

3. **Poor Error Visibility**
   - **Problem**: Sync failures weren't properly tracked or visible
   - **Fix**: Added try/except blocks with proper SyncRun status updates and transaction handling
   - **Impact**: All sync attempts are now tracked with success/failure status

## Part 2 - Reliability Improvements

### Chosen Solution: Retry Handling with Exponential Backoff

Added retry logic to handle transient failures during sync operations:
- **Maximum retries**: 3 attempts
- **Backoff strategy**: Exponential (2^attempt seconds)
- **Failure tracking**: Detailed error messages in SyncRun
- **Implementation**: Retry logic is implemented in the sync service layer (`syncapp/services.py`)

This choice provides resilience against temporary network issues or external system unavailability while avoiding endless retry loops.

## Part 3 - API Improvements

Enhanced the tasks API to support:
- Filtering by status via `?status=` query parameter
- Text search via `?search=` query parameter  
- Safe task deletion via `DELETE /api/tasks/<id>/` endpoint

## Part 4 - Quality Improvements

### Automated Tests
Added 5 comprehensive tests covering:
- Task creation during sync
- Task updates (idempotency)
- Sync run status tracking
- Task filtering by status
- Task search functionality

### Code Structure
- Separated concerns between services and views
- Added proper transaction handling
- Improved error handling throughout the application

## Frontend Enhancements

### Added Features
- **Retry Button**: Appears automatically when sync fails, allows users to retry failed syncs
- **Delete Tasks**: Individual delete buttons for each task with confirmation dialog
- **Better Error Handling**: User-friendly success/error messages with auto-dismiss
- **Visual Feedback**: Color-coded messages and button states

## Assumptions

1. **External System**: Simulated with static data in `fetch_external_tasks()`
2. **Database**: SQLite is sufficient for this challenge (no complex migrations needed)
3. **Authentication**: Not required as per challenge constraints
4. **Frontend Framework**: Plain HTML/JS is sufficient, no need for complex frameworks

## Tradeoffs

1. **Simplicity vs Features**: Kept the solution simple and focused on core requirements
2. **Retry Strategy**: Used exponential backoff but capped at 3 retries to avoid infinite loops
3. **Frontend**: Enhanced existing dashboard rather than rebuilding with a framework
4. **Testing**: Focused on critical path testing rather than exhaustive coverage

## Next Steps

If given more time, I would:

1. **Add Real-time Updates**: Implement WebSocket or Server-Sent Events for live sync status
2. **Export Functionality**: Add CSV/JSON export for tasks
3. **Bulk Operations**: Add bulk delete and bulk sync capabilities
4. **Monitoring**: Add detailed logging and metrics collection
5. **API Documentation**: Add OpenAPI/Swagger documentation
6. **Docker Support**: Containerize the application for easier deployment
7. **Rate Limiting**: Add API rate limiting to prevent abuse
8. **Task History**: Track task changes over time for audit trail

## Submission

This implementation meets all challenge requirements:
- Part 1: Fixed 3 critical bugs
- Part 2: Added retry handling for reliability
- Part 3: Enhanced tasks API with filtering
- Part 4: Added automated tests and improved structure
- Frontend: Added retry, delete, and better error handling
- Multiple meaningful commits with clear progression
- Project runs locally with proper setup instructions
