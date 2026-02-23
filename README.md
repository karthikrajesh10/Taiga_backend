

🚀 Taiga Clone Backend

Agile Project Management REST API (Django + DRF + PostgreSQL + JWT)

A production-ready REST API backend inspired by Taiga, built for
managing:

-   Projects
-   Sprints
-   User Stories
-   Tasks
-   Issues
-   Role-Based Access Control (RBAC)

------------------------------------------------------------------------

🛠 Tech Stack

-   Django 5
-   Django REST Framework
-   PostgreSQL
-   JWT Authentication (SimpleJWT)
-   Role-Based Access Control (RBAC)
-   CORS Support

------------------------------------------------------------------------

📦 Installation Guide

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

Make sure PostgreSQL is installed and running.

------------------------------------------------------------------------

Create Database & User

    psql -U postgres

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

If migrations conflict or tables already exist:

    psql -U postgres

    DROP DATABASE taiga_clone;
    CREATE DATABASE taiga_clone OWNER taiga_user;

Then:

    python manage.py migrate

⚠ This permanently deletes all data. Use only in development.

------------------------------------------------------------------------

🔐 Environment Variables (.env)

Create a .env file in the project root:

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

⚙ Run Migrations

    python manage.py makemigrations
    python manage.py migrate

------------------------------------------------------------------------

👤 Create Admin User

    python manage.py createsuperuser

------------------------------------------------------------------------

▶ Run Development Server

    python manage.py runserver

Server runs at:

    http://127.0.0.1:8000/

------------------------------------------------------------------------

🔐 Authentication (JWT)

This backend uses JWT authentication.

------------------------------------------------------------------------

🔹 Login

POST /api/token/

Sample Request

    {
      "username": "your_username",
      "password": "your_password"
    }

Sample Response

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

🔐 Required Header (For All Protected APIs)

    Authorization: Bearer <access_token>

------------------------------------------------------------------------

👤 Users API

  Endpoint             Method   Description
  -------------------- -------- --------------------------------
  /api/users/signup/   POST     Register new user
  /api/users/me/       GET      Get logged-in user
  /api/users/          GET      List all users (PM & MGR only)

------------------------------------------------------------------------

📁 Projects API

  Endpoint         Method
  ---------------- -----------
  /api/projects/   GET, POST

------------------------------------------------------------------------

🏃 Sprints API

  Endpoint        Method
  --------------- -----------
  /api/sprints/   GET, POST

------------------------------------------------------------------------

📘 User Stories API

  Endpoint                 Method
  ------------------------ -----------
  /api/userstories/        GET, POST
  /api/userstories/{id}/   PATCH

------------------------------------------------------------------------

📋 Tasks API

  Endpoint           Method
  ------------------ -----------
  /api/tasks/        GET, POST
  /api/tasks/{id}/   PATCH
  /api/tasks/my/     GET

------------------------------------------------------------------------

🐞 Issues API

  Endpoint       Method
  -------------- -----------
  /api/issues/   GET, POST

------------------------------------------------------------------------

🔢 Status Values (Frontend Mapping Required)

  Value   Meaning
  ------- ----------------
  1       New
  2       In Progress
  3       Ready For Test
  4       Done

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

------------------------------------------------------------------------

🔎 Special Access Rule

GET /api/users/

Accessible only by:

-   PM
-   MGR

Others receive:

    403 Forbidden

------------------------------------------------------------------------

🚫 Error Handling

  Status Code   Meaning
  ------------- --------------------------------------
  400           Bad Request
  401           Unauthorized (Invalid/Expired Token)
  403           Permission Denied

Frontend should:

-   Redirect to login on 401
-   Show permission message on 403

------------------------------------------------------------------------

🌐 CORS (Development Only)

    CORS_ALLOW_ALL_ORIGINS = True

⚠ In production, restrict allowed origins.

------------------------------------------------------------------------

🧱 Production Deployment Checklist

Before deploying:

-   Set DEBUG=False
-   Configure proper ALLOWED_HOSTS
-   Use strong DB password
-   Use secure SECRET_KEY
-   Configure HTTPS
-   Use Gunicorn
-   Use Nginx
-   Disable CORS_ALLOW_ALL_ORIGINS

------------------------------------------------------------------------

📂 Project Structure

    core/
    │
    ├── core/              # Project settings
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
