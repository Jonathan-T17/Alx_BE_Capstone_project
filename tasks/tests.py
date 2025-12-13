from django.test import TestCase

# Create your tests here.
# tasks/tests.py
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.utils import timezone
from users.models import User
from projects.models import Project
from tasks.models import Task

class TaskFlowTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="u1", email="u1@example.com", password="Passw0rd!")
        self.user2 = User.objects.create_user(username="u2", email="u2@example.com", password="Passw0rd!")
        # create project
        self.client.login(username="u1", password="Passw0rd!")  # optional; we'll use token auth in full tests

    def test_create_task(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("task-list")
        data = {
            "title": "Test Task",
            "description": "A test task",
            "priority": "MEDIUM",
            "status": "PENDING",
            "due_date": (timezone.now() + timezone.timedelta(days=2)).isoformat()
        }
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", resp.data)

    def test_assign_and_complete(self):
        self.client.force_authenticate(user=self.user)
        url = reverse("task-list")
        data = {
            "title": "Assign Task",
            "description": "assign to user2",
            "priority": "HIGH",
            "due_date": (timezone.now() + timezone.timedelta(days=3)).isoformat()
        }
        resp = self.client.post(url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        task_id = resp.data["id"]
        assign_url = reverse("task-assign", args=[task_id])
        resp2 = self.client.post(assign_url, {"assignees": [str(self.user2.id)]}, format="json")
        self.assertEqual(resp2.status_code, status.HTTP_200_OK)

        complete_url = reverse("task-complete", args=[task_id])
        resp3 = self.client.post(complete_url, {"completed": True}, format="json")
        self.assertEqual(resp3.status_code, status.HTTP_200_OK)
        # fetch task
        resp4 = self.client.get(reverse("task-detail", args=[task_id]), format="json")
        self.assertEqual(resp4.data["status"], "COMPLETED")
