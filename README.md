📘 Taiga Clone Backend (Django + PostgreSQL + JWT)

A REST API backend for a Taiga-inspired Agile Project Management system
built using:

-   Django 5
-   Django REST Framework
-   PostgreSQL
-   JWT Authentication (SimpleJWT)

------------------------------------------------------------------------

🚀 1. Clone the Repository

    git clone https://github.com/karthikrajesh10/Taiga_backend.git
    cd Taiga_backend

------------------------------------------------------------------------

🐍 2. Create & Activate Virtual Environment

Windows:

    python -m venv venv
    venv\Scripts\activate

Mac/Linux:

    python3 -m venv venv
    source venv/bin/activate

------------------------------------------------------------------------

📦 3. Install Required Packages

    pip install -r requirements.txt

If installing manually, required core packages are:

    pip install django
    pip install djangorestframework
    pip install djangorestframework-simplejwt
    pip install psycopg2-binary
    pip install django-cors-headers
    pip install python-dotenv

------------------------------------------------------------------------

🐘 4. PostgreSQL Setup

Make sure PostgreSQL is installed and running.

------------------------------------------------------------------------

🔹 4.1 Login to PostgreSQL

    psql -U postgres

If password prompted, enter your postgres password.

------------------------------------------------------------------------

🔹 4.2 Create Database & User

Inside psql shell:

    CREATE DATABASE taiga_clone;

    CREATE USER taiga_user WITH PASSWORD 'strongpassword';

    ALTER ROLE taiga_user SET client_encoding TO 'utf8';
    ALTER ROLE taiga_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE taiga_user SET timezone TO 'UTC';

    GRANT ALL PRIVILEGES ON DATABASE taiga_clone TO taiga_user;

Exit:

    \q

------------------------------------------------------------------------

🔐 5. Environment Variables Setup (.env)

Create a file in the project root (same level as manage.py):

    .env

Add the following:

    # =============================
    # DJANGO SETTINGS
    # =============================

    SECRET_KEY=your-generated-secret-key
    DEBUG=True
    ALLOWED_HOSTS=127.0.0.1,localhost

    # =============================
    # DATABASE CONFIG
    # =============================

    DB_NAME=taiga_clone
    DB_USER=taiga_user
    DB_PASSWORD=strongpassword
    DB_HOST=localhost
    DB_PORT=5432

    # =============================
    # JWT CONFIG
    # =============================

    ACCESS_TOKEN_MINUTES=60
    REFRESH_TOKEN_DAYS=1

------------------------------------------------------------------------

🔹 Generate SECRET_KEY

Run:

    python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

Copy the output into .env.

------------------------------------------------------------------------

⚙ 6. Apply Migrations

    python manage.py makemigrations
    python manage.py migrate

------------------------------------------------------------------------

👤 7. Create Superuser (Admin)

    python manage.py createsuperuser

Enter:

-   Username
-   Email
-   Password

------------------------------------------------------------------------

▶ 8. Run the Development Server

    python manage.py runserver

Server runs at:

    http://127.0.0.1:8000/

------------------------------------------------------------------------

🔑 9. Authentication Flow (JWT)

🔹 Obtain Token

    POST /api/token/

Body:

    {
      "username": "admin",
      "password": "yourpassword"
    }

Response:

    {
      "refresh": "...",
      "access": "..."
    }

------------------------------------------------------------------------

🔹 Use Access Token

Add header in requests:

    Authorization: Bearer <access_token>

------------------------------------------------------------------------

📂 Project Structure

    core/
    │
    ├── core/                 # Project settings
    ├── projects/             # Project & Membership logic
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

🔐 Security Notes

-   .env file is excluded via .gitignore
-   SECRET_KEY is not committed
-   Database credentials are environment-based
-   JWT authentication enabled
-   Default permission: IsAuthenticated

------------------------------------------------------------------------

🌐 CORS Configuration

Currently allows all origins for development:

    CORS_ALLOW_ALL_ORIGINS = True

⚠ For production, restrict allowed origins.

------------------------------------------------------------------------

🧪 Useful API Endpoints

  Endpoint              Description
  --------------------- ------------------------
  /api/token/           Login
  /api/token/refresh/   Refresh token
  /api/users/me/        Get logged-in user
  /api/projects/        List/Create projects
  /api/memberships/     Manage project members
  /api/sprints/         Sprint management
  /api/userstories/     Backlog management

------------------------------------------------------------------------

🧱 Production Deployment Checklist

Before deploying:

-   Set DEBUG=False
-   Set real ALLOWED_HOSTS
-   Use strong DB password
-   Use secure SECRET_KEY
-   Configure HTTPS
-   Use Gunicorn + Nginx

------------------------------------------------------------------------

🛠 Development Workflow

    # Activate venv
    venv\Scripts\activate

    # Run server
    python manage.py runserver

    # Make migrations
    python manage.py makemigrations
    python manage.py migrate

------------------------------------------------------------------------

👨‍💻 Author

Karthik R S 

------------------------------------------------------------------------

