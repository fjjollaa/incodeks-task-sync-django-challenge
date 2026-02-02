from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import sync_tasks
from .models import Task, SyncRun
from .serializers import TaskSerializer, SyncRunSerializer
from django.views.generic import TemplateView

class DashboardView(TemplateView):
    template_name = "syncapp/dashboard.html"


class TriggerSyncView(APIView):
    def post(self, request):
        sync_tasks()
        return Response({"status": "sync triggered"}, status=status.HTTP_200_OK)

class TaskListView(APIView):
    def get(self, request):
        qs = Task.objects.all().order_by("-updated_at")
        
        status_filter = request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        
        search = request.query_params.get('search')
        if search:
            qs = qs.filter(title__icontains=search)
        
        return Response(TaskSerializer(qs, many=True).data)

class LastSyncStatusView(APIView):
    def get(self, request):
        last = SyncRun.objects.order_by("-started_at").first()
        if not last:
            return Response({"status": "no sync yet"}, status=status.HTTP_200_OK)
        return Response(SyncRunSerializer(last).data, status=status.HTTP_200_OK)


class TaskDeleteView(APIView):
    def delete(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            task.delete()
            return Response({"status": "deleted"}, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({"error": "Task not found"}, status=status.HTTP_404_NOT_FOUND)