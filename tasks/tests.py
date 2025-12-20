# tasks/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from tasks.models import Task, TaskAssignment

User = get_user_model()


class TaskAPITests(APITestCase):

    def setUp(self):
        """
        Create users and authenticate
        """
        self.user = User.objects.create_user(
            username="user1",
            email="user1@test.com",
            password="UserPass123"
        )

        self.other_user = User.objects.create_user(
            username="user2",
            email="user2@test.com",
            password="UserPass123"
        )

        self.client.force_authenticate(user=self.user)

        self.task_list_url = "/api/tasks/"

        self.task = Task.objects.create(
            title="Test Task",
            description="Task description",
            creator=self.user,
            due_date=timezone.now() + timedelta(days=2),
        )

    # -------------------------
    # TASK CREATION
    # -------------------------

    def test_create_task(self):
        data = {
            "title": "New Task",
            "description": "New task description",
            "priority": "HIGH",
            "status": "PENDING",
            "due_date": (timezone.now() + timedelta(days=3)).isoformat()
        }

        response = self.client.post(self.task_list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Task")

    def test_task_due_date_must_be_future(self):
        data = {
            "title": "Invalid Task",
            "due_date": (timezone.now() - timedelta(days=1)).isoformat()
        }

        response = self.client.post(self.task_list_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -------------------------
    # TASK RETRIEVAL
    # -------------------------

    def test_user_can_view_own_tasks(self):
        response = self.client.get(self.task_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(all(task["creator"] == str(self.user.id) for task in response.data["results"]))#hhhhhh


    def test_user_cannot_see_others_tasks(self):
        Task.objects.create(
            title="Other Task",
            creator=self.other_user,
            due_date=timezone.now() + timedelta(days=1)
        )

        response = self.client.get(self.task_list_url)
        self.assertTrue(all(task["creator"] == str(self.user.id) for task in response.data["results"])) #kkkk


    # -------------------------
    # TASK UPDATE
    # -------------------------

    def test_user_can_update_own_task(self):
        url = f"{self.task_list_url}{self.task.id}/"
        response = self.client.put(url, {
            "title": "Updated Task",
            "status": "IN_PROGRESS"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    def test_user_cannot_update_completed_task(self):
        self.task.status = Task.STATUS_COMPLETED
        self.task.save()

        url = f"{self.task_list_url}{self.task.id}/"
        response = self.client.put(url, {
            "title": "Try update"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -------------------------
    # TASK COMPLETION LOGIC
    # -------------------------

    def test_mark_task_completed_sets_timestamp(self):
        url = f"{self.task_list_url}{self.task.id}/"

        response = self.client.patch(url, {
            "status": "COMPLETED"
        }, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertIsNotNone(self.task.completed_at)

    def test_mark_task_incomplete_clears_timestamp(self):
        self.task.status = Task.STATUS_COMPLETED
        self.task.completed_at = timezone.now()
        self.task.save()
    
        url = f"{self.task_list_url}{self.task.id}/"
        response = self.client.put(
            url,
            {"status": Task.STATUS_PENDING},
            format="json"
        )
    
        self.task.refresh_from_db()
    
        if response.status_code == status.HTTP_200_OK:
            # Update allowed → timestamp must be cleared
            self.assertIsNone(self.task.completed_at)
            self.assertEqual(self.task.status, Task.STATUS_PENDING)
    
        elif response.status_code == status.HTTP_403_FORBIDDEN:
            # Update denied → timestamp must remain
            self.assertIsNotNone(self.task.completed_at)
            self.assertEqual(self.task.status, Task.STATUS_COMPLETED)
    
        else:
            self.fail(f"Unexpected status code: {response.status_code}")


    # -------------------------
    # TASK ASSIGNMENT
    # -------------------------

    def test_assign_user_to_task(self):
        assignment = TaskAssignment.objects.create(
            task=self.task,
            user=self.other_user,
            assigned_by=self.user
        )

        self.assertEqual(assignment.task, self.task)
        self.assertEqual(assignment.user, self.other_user)

    def test_duplicate_assignment_not_allowed(self):
        TaskAssignment.objects.create(
            task=self.task,
            user=self.other_user
        )

        with self.assertRaises(Exception):
            TaskAssignment.objects.create(
                task=self.task,
                user=self.other_user
            )

    # -------------------------
    # TASK DELETION
    # -------------------------

    def test_user_can_delete_own_task(self):
        url = f"{self.task_list_url}{self.task.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_user_cannot_delete_others_task(self):
        other_task = Task.objects.create(
            title="Other Task",
            creator=self.other_user,
            due_date=timezone.now() + timedelta(days=1)
        )

        url = f"{self.task_list_url}{other_task.id}/"
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
