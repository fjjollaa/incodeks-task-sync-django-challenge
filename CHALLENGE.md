# Incodeks Django Backend Coding Challenge - Production Scenario (Task Sync Service)

Welcome! This is a practical coding challenge that simulates joining a team to stabilize and extend an existing Django service.

## Context

You're joining a team that maintains a small backend service responsible for syncing tasks from an external system into our database.

The external system is simulated in this codebase (see `syncapp/services.py`). In a real scenario, this would be a third-party API that provides task data.

The service exists, runs, and mostly works, but we've seen issues in production:
- Duplicate records appearing
- Inconsistent sync results
- Poor visibility into failures

The codebase has known issues; part of the task is to find and fix them. Your task is to **stabilize the system and extend it slightly**, not to rebuild it from scratch.

## What we provide

This repository contains a Django + DRF service for task synchronization.

### Quick start

1. Follow the Setup steps below to get the app running locally.
2. Visit `http://127.0.0.1:8000/` to see the dashboard.
3. Review the codebase, especially `syncapp/services.py` and `syncapp/views.py`.
4. Start with Part 1 (code review) to understand the issues.

## Your tasks

Your README.md must include setup/run instructions and the sections described in Part 1, Part 2, Part 4, and Submission.

### Part 1 - Code review and improvements (required)
- Review the codebase thoroughly
- Identify and fix at least **three** bug or design issues you find
- In your README, include a section that explains:
  - what issues you identified
  - why they could cause problems
  - how your fixes address them

### Part 2 - Improve reliability (required)
Choose **one** and implement it:
- Make the sync idempotent
- Add basic retry handling for failed syncs
- Improve error logging / reporting so failures are visible

Explain your choice in your README.

### Part 3 - Small feature (required)
**Note:** Basic endpoints already exist, but they may need enhancement to meet the requirements below.

Enhance or create **one** of the following:
- An API endpoint to trigger a manual sync **and return a meaningful result** (currently returns basic status)
- An API endpoint to list synced tasks **with basic filtering** (currently returns all tasks)
- A status endpoint showing the last sync result **with meaningful failure information** (currently returns basic status)

Keep it pragmatic. You can enhance existing endpoints or create new ones as needed.

### Part 4 - Quality (required)
- Add at least **one meaningful automated test**
- Improve code structure where needed (avoid overengineering)
- Your README must include:
  - assumptions
  - tradeoffs
  - what you would do next if you had more time

## Frontend requirement (required)

Note: A minimal dashboard page is provided at `/` that helps validate behavior. It already has: a button to trigger sync, a way to view the last sync status, and a way to list tasks.

You must add:
- Retry functionality for failed syncs
- Delete/remove tasks functionality
- Better error handling and user feedback

The dashboard uses plain HTML + JavaScript. **You are free to use any frontend tools or frameworks** to enhance this dashboard. You may adjust routing if you prefer `/dashboard/`, but keep it obvious.

### Bonus 1 - Optional frontend enhancements

If you have time, consider adding:
- Real-time status updates
- Keyboard shortcuts for common actions
- Export tasks (e.g. CSV)
- Dark mode or other UI polish

### Bonus 2 - Docker setup (optional)
If you have time, add a Docker setup so the service can be run locally via containers.

Include:
- `Dockerfile`
- `docker-compose.yml`

And document the commands in your README for:
- building and starting the stack
- running migrations
- running tests

## Constraints
- Use Python + Django (DRF is included)
- SQLite is acceptable for this challenge
- No authentication required
- No deployment required

## Time expectation

- **Core requirements (Parts 1-4 + Frontend):** ~4-5 hours
- **With optional enhancements:** ~5-6 hours

If you do not finish everything, explain your priorities.

## Setup

Python 3.8+ required.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py migrate
python manage.py runserver
```

Existing endpoints (may need enhancement):
- POST `http://127.0.0.1:8000/api/sync/` - Triggers sync (basic implementation)
- GET  `http://127.0.0.1:8000/api/tasks/` - Lists all tasks (no filtering)
- GET  `http://127.0.0.1:8000/api/sync/status/` - Shows last sync status (basic info)

## Submission
- **Due:** Tuesday Feb 3, 2026, 17:00 CET.
- Provide a **GitHub repository** (public or private) with your work in **multiple meaningful commits**. Please avoid a single large intial or final commit. Send us the repo link (e.g. by replying to the challenge email).
- Make sure it runs locally (`python manage.py migrate` then `python manage.py runserver`; run `python manage.py test` for your tests).
- Your **README.md** must include setup/run instructions and your decisions and reasoning.