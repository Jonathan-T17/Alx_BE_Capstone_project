# Alx_BE_Capstone_project

## Task Management API (Capstone) — Backend

**Status:** Part 3 (Models implemented)  
**ERD:** `sandbox:/mnt/data/task_management_api_erd_final.png`

---

## Project summary

This repository contains the backend for the **Task Management API** — a Django + Django REST Framework project for creating and managing projects, tasks, teams, users, roles & permissions, comments, and activity logs.

This work corresponds to **Capstone Part 3 (Start Building)**. In this milestone we implemented the complete data model layer (Django models) for the application.

---

## What was implemented (commits)

The following feature commits were completed in this phase:

- `feat(users): add custom User, Profile, PasswordResetToken`  
  - Custom `User` model (UUID PK, email unique, role FK)
  - `Profile` (1:1 with User): phone, job_title, department, avatar_url
  - `PasswordResetToken` for secure password reset flow

- `feat(roles): add Role, Permission, RolePermission`  
  - `Role` entity (Admin, Manager, Staff, User)
  - `Permission` entity (granular permission codes)
  - `RolePermission` pivot table (M2M between roles & permissions)

- `feat(projects): add Project model`  
  - `Project` with `owner`, start/end dates, timestamps and indexes

- `feat(tasks): add Task, TaskAssignment, Comment`  
  - `Task` with priority, status, due_date, completed_at and business validations  
  - `TaskAssignment` pivot table for many-to-many task assignees  
  - `Comment` for task discussions

- `feat(teams): add Team and TeamMember`  
  - `Team` entity with a manager  
  - `TeamMember` pivot table for member relations

- `feat(activity): add ActivityLog`  
  - `ActivityLog` to record major events (login, create/update task, assign, complete, etc.)

---

main app:
users: add custom User, Profile,PasswordResetToken

roles: add Role, Permission, RolePermission

projects: add Project model

tasks: add Task, TaskAssignment, Comment

teams: add Team and TeamMember

activity: add ActivityLog
