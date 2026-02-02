import random
from django.utils import timezone
from django.db import transaction
from .models import Task, SyncRun

def fetch_external_tasks():
    # Simulates fetching tasks from an external system.
    # In a real setup this would call a third-party API.
    return [
        {"id": "ext-1", "title": "Task A", "status": "todo"},
        {"id": "ext-2", "title": "Task B", "status": "done"},
    ]

def sync_tasks():
    """Sync tasks into DB."""
    run = SyncRun.objects.create(status="running")
    
    try:
        tasks = fetch_external_tasks()
        
        with transaction.atomic():
            for t in tasks:
                Task.objects.update_or_create(
                    external_id=t["id"],
                    defaults={
                        "title": t["title"],
                        "status": t["status"]
                    }
                )

        # Simulate potential external system errors
        if random.choice([True, False]):
            run.status = "failed"
            run.message = "Random sync failure"
            run.finished_at = timezone.now()
            run.save()
            raise Exception("Random sync failure")

        run.status = "success"
        run.finished_at = timezone.now()
        run.save()
        return run
        
    except Exception as e:
        run.status = "failed"
        run.message = str(e)
        run.finished_at = timezone.now()
        run.save()
        raise
