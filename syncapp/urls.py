from django.urls import path
from .views import TriggerSyncView, TaskListView, LastSyncStatusView

urlpatterns = [
    path("sync/", TriggerSyncView.as_view(), name="trigger-sync"),
    path("tasks/", TaskListView.as_view(), name="list-tasks"),
    path("sync/status/", LastSyncStatusView.as_view(), name="last-sync-status"),
]
