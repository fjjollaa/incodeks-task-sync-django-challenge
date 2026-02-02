from rest_framework import serializers
from .models import Task, SyncRun

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id", "external_id", "title", "status", "updated_at"]

class SyncRunSerializer(serializers.ModelSerializer):
    class Meta:
        model = SyncRun
        fields = ["id", "started_at", "finished_at", "status", "message"]
