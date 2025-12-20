# Task Management API – Capstone Project

## Project Purpose

-> This project is a Task Management REST API built with Django Rest Framework.

-> The goal of this project is to help individuals or organizations manage projects, tasks, and users securely using role-based access and JWT authentication.

## ->It allows users to

--Register and authenticate securely

--Manage projects

--Create, assign, and complete tasks

--Enforce business rules and permissions

--Track activity

>>>> It supports both individual users and organization-based usage.

## It supports both

--Individual users

--Organization-based management

## 🛠️ Technology Stack

--Python

--Django

--Django REST Framework

--Simple JWT

--SQLite (development)

--postgresql(production)

--Postman (API testing)

## Authentication System

>>> This API is secured using JWT authentication.
Most endpoints require a valid token, which prevents unauthorized access.
>>> I will first show what happens when authentication is missing, then show the correct way.

## brief mainly important of this TASK MANAGEMENT API

>>> Is to solve the problem of organizing tasks, assigning responsibilities, tracking completion, and managing projects in a structured and secure way.

-->The API uses JWT (JSON Web Tokens).

--Public Endpoints(this can be used by user during registration and login inorder toget access to the system).

--Endpoint                    Method     Description
-->>/api/auth/       POST       User self-registration
-->>/api/auth/token/          POST       Login & get token
-->>/api/auth/token/refresh/  POST       Refresh token
-->>Protected Endpoints

## All others require are the following

>>>>>Authorization: Bearer <access_token>

## Demo Flow

## 1️⃣ User Registration: POST /api/auth/

{
  "username": "Jonathan1",
  "email": "jonathan11@example.com",
  "password": "StrongPassword123",
  "password2": "StrongPassword123"
}


## ✔ Allows individual users to onboard themselves

## 2️⃣ User Login: POST /api/auth/token/

{
  "username": "Jonathan"1,
  "password": "StrongPassword123"
}

## Response includes

1. access

2. refresh

## 3️⃣ Authorization Header

## All protected requests must include:

>>>> Authorization: Bearer <access_token>


## Without this → 401 Unauthorized

## 4️⃣ Create a Project: POST /api/projects/

{
  "name": "Demo Project",
  "description": "Capstone demo project"
}


>>>>> ✔ Save the returned id (UUID).

## 5️⃣ Create a Task: POST /api/tasks/

{
  "name": "Build API",
  "description": "Implement task endpoints",
  "priority": "HIGH",
  "status": "PENDING",
  "project": "PROJECT_UUID",
  "due_date": "2026-01-10T12:00:00Z"
}

## Common Error Explained

“<project_id>” is not a valid UUID

## ✔ Fix: Use the real project UUID returned after creating projects above

## 6️⃣ Assign Users to Task: POST /api/tasks/{task_id}/assign/

{
  "assignees": ["USER_UUID"]
}

## ✔ Permission-controlled

## ✔ Logged as activity

## 7️⃣ Complete a Task: POST /api/tasks/{task_id}/complete/

{
  "completed": true
}

## ✔ Status set to COMPLETED

## ✔ completed_at timestamp added

## ✔ Task becomes read-only

### 8️⃣ Revert Task Completion

## Only creator or admin

{
  "completed": false
}

## ✔ Clears timestamp

## ✔ Allows editing again

## 9️⃣ Permissions & Security

>>>> Unauthorized browser access → Blocked
>>> JWT required for all sensitive operations
>> Users only see tasks they own or are assigned

## 🧪 Testing

Run all tests:  python manage.py test

## ✔ Permissions

## ✔ Task rules

## ✔ Status logic

## All tests pass successfully
