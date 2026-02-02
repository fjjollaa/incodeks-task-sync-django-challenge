from django.urls import path
from .views import TriggerSyncView, TaskListView, LastSyncStatusView, TaskDeleteView

urlpatterns = [
    path("sync/", TriggerSyncView.as_view(), name="trigger-sync"),
    path("tasks/", TaskListView.as_view(), name="list-tasks"),
    path("tasks/<int:task_id>/", TaskDeleteView.as_view(), name="delete-task"),
    path("sync/status/", LastSyncStatusView.as_view(), name="last-sync-status"),
]
