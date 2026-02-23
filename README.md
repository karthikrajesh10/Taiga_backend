------------------------------------------------------------------------

🚀 Taiga Clone Backend

Agile Project Management REST API

Built with Django 5 + Django REST Framework + PostgreSQL + JWT

------------------------------------------------------------------------

📌 Overview

Taiga Clone Backend is a production-ready REST API for managing:

-   👤 Users
-   📁 Projects
-   🏃 Sprints
-   📘 User Stories
-   📋 Tasks
-   🐞 Issues
-   🔐 Role-Based Access Control (RBAC)

Authentication is handled using JWT (JSON Web Tokens).

------------------------------------------------------------------------

🛠 Tech Stack

-   Django 5
-   Django REST Framework
-   PostgreSQL
-   SimpleJWT
-   RBAC (Custom Role Permissions)
-   CORS Support

------------------------------------------------------------------------

⚙ Installation Guide

------------------------------------------------------------------------

1️⃣ Clone Repository

    git clone https://github.com/karthikrajesh10/Taiga_backend.git
    cd Taiga_backend

------------------------------------------------------------------------

2️⃣ Create Virtual Environment

Windows

    python -m venv venv
    venv\Scripts\activate

Mac/Linux

    python3 -m venv venv
    source venv/bin/activate

------------------------------------------------------------------------

3️⃣ Install Dependencies (Compulsory)

Install Individually

    pip install django
    pip install djangorestframework
    pip install djangorestframework-simplejwt
    pip install psycopg2-binary
    pip install django-cors-headers
    pip install python-dotenv

✅ Install All In One Command

    pip install django djangorestframework djangorestframework-simplejwt psycopg2-binary django-cors-headers python-dotenv

Or:

    pip install -r requirements.txt

------------------------------------------------------------------------

🐘 PostgreSQL Setup

Login:

    psql -U postgres

Create database and user:

    CREATE DATABASE taiga_clone;

    CREATE USER taiga_user WITH PASSWORD 'strongpassword';

    ALTER ROLE taiga_user SET client_encoding TO 'utf8';
    ALTER ROLE taiga_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE taiga_user SET timezone TO 'UTC';

    GRANT ALL PRIVILEGES ON DATABASE taiga_clone TO taiga_user;
    GRANT ALL ON SCHEMA public TO taiga_user;

Exit:

    \q

------------------------------------------------------------------------

🗑 Reset Database (If Tables Already Exist)

If migrations conflict:

    psql -U postgres

    DROP DATABASE taiga_clone;
    CREATE DATABASE taiga_clone OWNER taiga_user;

Then:

    python manage.py migrate

⚠ This deletes all data (development use only).

------------------------------------------------------------------------

🔐 Environment Variables (.env)

Create .env file in project root:

    # DJANGO
    SECRET_KEY=your-generated-secret-key
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost

    # DATABASE
    DB_NAME=taiga_clone
    DB_USER=taiga_user
    DB_PASSWORD=strongpassword
    DB_HOST=localhost
    DB_PORT=5432

    # JWT
    ACCESS_TOKEN_MINUTES=60
    REFRESH_TOKEN_DAYS=1

Generate secret key:

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

------------------------------------------------------------------------

🔄 Run Migrations

    python manage.py makemigrations
    python manage.py migrate

------------------------------------------------------------------------

👤 Create Superuser

    python manage.py createsuperuser

------------------------------------------------------------------------

▶ Run Development Server

    python manage.py runserver

Server runs at:

    http://127.0.0.1:8000/

------------------------------------------------------------------------

🔐 Authentication (JWT)

Base URL:

    http://127.0.0.1:8000/

All protected endpoints require:

    Authorization: Bearer <access_token>

------------------------------------------------------------------------

🔹 Login

POST /api/token/

Request

    {
      "username": "your_username",
      "password": "your_password"
    }

Response

    {
      "refresh": "refresh_token_here",
      "access": "access_token_here"
    }

------------------------------------------------------------------------

🔹 Refresh Token

POST /api/token/refresh/

    {
      "refresh": "refresh_token_here"
    }

------------------------------------------------------------------------

📡 API Documentation

------------------------------------------------------------------------

👤 Users API

🔹 Signup

POST /api/users/signup/ Permission: Public

    {
      "username": "your_username",
      "email": "your_gmail",
      "password": "your_password",
      "role": "DEV"
    }

------------------------------------------------------------------------

🔹 Get Logged-in User

GET /api/users/me/ Permission: Authenticated Users

------------------------------------------------------------------------

🔹 Get All Users

GET /api/users/ Permission: PM, MGR only

Response:

    [
      {
        "id": 1,
        "username": "manager1",
        "email": "m@test.com",
        "role": "MGR"
      }
    ]

------------------------------------------------------------------------

📁 Projects API

🔹 Create Project

POST /api/projects/ Permission: PM only

    {
      "name": "Backend System",
      "slug": "backend-system",
      "description": "Core PM Tool",
      "is_private": false
    }

------------------------------------------------------------------------

🔹 List Projects

GET /api/projects/ Permission: Authenticated Users

------------------------------------------------------------------------

🏃 Sprints API

🔹 Create Sprint

POST /api/sprints/ Permission: MGR only

    {
      "name": "Sprint 1",
      "slug": "sprint-1",
      "project_slug": "backend-system",
      "start_date": "2026-02-16",
      "end_date": "2026-02-28"
    }

------------------------------------------------------------------------

📘 User Stories API

🔹 Create Story

POST /api/userstories/ Permission: MGR only

    {
      "title": "Implement Login",
      "slug": "implement-login",
      "description": "JWT login feature",
      "priority": 1,
      "project_slug": "backend-system"
    }

------------------------------------------------------------------------

🔹 Move Story to Sprint

PATCH /api/userstories/{id}/

    {
      "sprint": 1
    }

------------------------------------------------------------------------

📋 Tasks API

🔹 Create Task

POST /api/tasks/ Permission: MGR only

    {
      "user_story": 1,
      "title": "Create JWT Endpoint",
      "description": "Implement token endpoint"
    }

------------------------------------------------------------------------

🔹 Update Task

PATCH /api/tasks/{id}/

Example:

    {
      "status": 2
    }

------------------------------------------------------------------------

🔹 Get My Tasks

GET /api/tasks/my/ Permission: Authenticated Users

Example:

    [
      {
        "id": 1,
        "user_story": 1,
        "title": "Create JWT Endpoint",
        "status": 3,
        "assignee": 4,
        "created_at": "2026-02-16T09:53:19Z"
      }
    ]

------------------------------------------------------------------------

🐞 Issues API

🔹 Create Issue

POST /api/issues/

Permission:

-   Bug → QA, TL
-   Question/Enhancement → All roles

    {
      "task": 1,
      "type": "Bug",
      "title": "Token expires early",
      "description": "Access token expires too fast"
    }

------------------------------------------------------------------------

🔢 Status Values

  Value   Meaning
  ------- ----------------
  1       New
  2       In Progress
  3       Ready For Test
  4       Done

Frontend must map numeric values to UI labels.

------------------------------------------------------------------------

🔐 Role-Based Access Control (RBAC)

🎭 Roles

  Code   Role
  ------ -----------------
  PM     Project Manager
  MGR    Manager
  DEV    Developer
  QA     Quality Analyst
  TL     Team Lead
  AP     Approver

------------------------------------------------------------------------

🛡 Permission Matrix

  ----------------------------------------------------------------------------------
  Action                                             PM   MGR   DEV   QA   TL   AP
  -------------------------------------------------- ---- ----- ----- ---- ---- ----
  Create User                                        ✅   ❌    ❌    ❌   ❌   ❌

  Assign Project                                     ✅   ❌    ❌    ❌   ❌   ❌

  Create Sprint                                      ❌   ✅    ❌    ❌   ❌   ❌

  Create Story                                       ❌   ✅    ❌    ❌   ❌   ❌

  Create Task                                        ❌   ✅    ❌    ❌   ❌   ❌

  Assign Task                                        ❌   ✅    ❌    ❌   ❌   ❌

  Estimate Hours                                     ❌   ❌    ✅    ❌   ❌   ❌

  Move Task Status                                   ❌   ❌    ✅    ❌   ❌   ❌

  Create Issue (Bug)                                 ❌   ❌    ❌    ✅   ✅   ❌

  Create Issue (Question/Enhancement)                ✅   ✅    ✅    ✅   ✅   ✅

  Approve Document                                   ❌   ❌    ❌    ❌   ❌   ✅
  ----------------------------------------------------------------------------------

Special Rule: GET /api/users/ accessible only by PM and MGR.

------------------------------------------------------------------------

🚫 Error Handling

  Code   Meaning
  ------ --------------------------------------
  400    Validation error
  401    Unauthorized (Token missing/expired)
  403    Permission denied
  404    Resource not found

------------------------------------------------------------------------

🌐 CORS (Development Only)

    CORS_ALLOW_ALL_ORIGINS = True

⚠ Restrict origins in production.

------------------------------------------------------------------------

🧱 Production Deployment Checklist

-   Set DEBUG=False
-   Configure proper ALLOWED_HOSTS
-   Use strong DB password
-   Use secure SECRET_KEY
-   Enable HTTPS
-   Use Gunicorn
-   Use Nginx
-   Restrict CORS

------------------------------------------------------------------------

📂 Project Structure

    core/
    │
    ├── core/
    ├── projects/
    ├── sprints/
    ├── userstories/
    ├── tasks/
    ├── issues/
    ├── users/
    │
    ├── manage.py
    ├── requirements.txt
    └── .env

------------------------------------------------------------------------

👨‍💻 Author

Karthik R S

------------------------------------------------------------------------
