from django.test import TestCase
from unittest.mock import patch
from .models import Task, SyncRun
from .services import sync_tasks


class SyncTasksTest(TestCase):
    
    def test_sync_creates_tasks(self):
        self.assertEqual(Task.objects.count(), 0)
        
        with patch('syncapp.services.random.choice', return_value=False):
            sync_tasks()
        
        self.assertEqual(Task.objects.count(), 2)
        self.assertTrue(Task.objects.filter(external_id="ext-1").exists())
        self.assertTrue(Task.objects.filter(external_id="ext-2").exists())
    
    def test_sync_updates_existing_tasks(self):
        Task.objects.create(external_id="ext-1", title="Old Title", status="todo")
        
        with patch('syncapp.services.random.choice', return_value=False):
            sync_tasks()
        
        task = Task.objects.get(external_id="ext-1")
        self.assertEqual(task.title, "Task A")
    
    def test_sync_run_status_on_success(self):
        with patch('syncapp.services.random.choice', return_value=False):
            run = sync_tasks()
        
        self.assertEqual(run.status, "success")
        self.assertIsNotNone(run.finished_at)


class TaskFilteringTest(TestCase):
    
    def setUp(self):
        Task.objects.create(external_id="t1", title="First Task", status="todo")
        Task.objects.create(external_id="t2", title="Second Task", status="done")
    
    def test_filter_by_status(self):
        response = self.client.get('/api/tasks/?status=todo')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
    
    def test_search_by_title(self):
        response = self.client.get('/api/tasks/?search=First')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
