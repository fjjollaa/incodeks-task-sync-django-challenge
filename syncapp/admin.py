from django.contrib import admin
from .models import Task, SyncRun

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "external_id", "title", "status", "updated_at")
    search_fields = ("external_id", "title", "status")

@admin.register(SyncRun)
class SyncRunAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "started_at", "finished_at")
    search_fields = ("status",)
