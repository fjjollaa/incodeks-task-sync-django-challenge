from django.db import models

class Task(models.Model):
    external_id = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=32)  # todo, in_progress, done (not enforced)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.external_id}: {self.title}"

class SyncRun(models.Model):
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=32, default="unknown")  # success/failed
    message = models.TextField(blank=True, default="")

    def __str__(self):
        return f"SyncRun({self.id}) {self.status}"
