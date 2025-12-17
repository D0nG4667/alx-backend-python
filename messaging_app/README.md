# 📬 messaging_app

A modular, containerized Django backend for real-time messaging between users. Built with Django REST Framework, custom user roles, and clean API architecture.

---

## 🚀 Features

- Custom `User` model with UUID primary key, role enum, and secure password hashing
- RESTful endpoints for creating and retrieving messages and conversations
- Many-to-many conversation tracking between users
- Dockerized development environment with `docker-compose`
- Configurable via `.env.example` for environment-specific settings
- Linting and dependency management via `pyproject.toml` and `ruff.toml`

---

## 🧱 Tech Stack

- **Backend:** Django + Django REST Framework
- **Auth:** Custom user model with email-based login
- **Database:** MySQL (via Docker)
- **Containerization:** Docker & docker-compose
- **Linting:** Ruff
- **Config:** `.env`, `pyproject.toml`, `ruff.toml`

---

### 🛠️ Setup Instructions

#### 1. Clone the repository

```bash
git clone https://github.com/D0nG4667/alx-backend-python.git
cd alx-backend-python/messaging_app
```

#### 2. Configure environment

```bash
cp .env.example .env
# Update database credentials and secret key
```

#### 3. Build and run with Docker

```bash
docker-compose up --build
```

#### 4. Run migrations

```bash
docker-compose exec web python manage.py makemigrations chats
docker-compose exec web python manage.py migrate
```

---

### 📚 API Overview

| Endpoint                  | Method | Description                     |
|--------------------------|--------|---------------------------------|
| `/api/messages/`         | GET/POST | List or create messages         |
| `/api/conversations/`    | GET/POST | List or create conversations    |
| `/admin/`                | GET    | Django admin panel              |

---

### 👤 User Roles

- `guest`: Basic messaging access
- `host`: Can initiate conversations
- `admin`: Full access via Django admin

---

### 📦 Project Structure

```folder
messaging_app/
├── chats/               # Models, views, serializers for messaging
├── messaging_app/       # Core Django project settings
├── Dockerfile
├── docker-compose.yaml
├── .env.example
├── README.md
```

---

### 🧪 Testing

```bash
docker-compose exec web python manage.py test
```

## 📑 DevOps & CI/CD Journey

Over the course of this project, I established a complete pipeline that takes the messaging app from source code to tested, linted, and containerized deployment. Here’s the path I followed:

### Task 0 – Jenkins Foundations

I began by running Jenkins inside a Docker container, installing essential plugins, and wiring up a pipeline that pulls code from GitHub, installs dependencies, runs pytest, and generates reports. This gave us a reproducible CI environment with manual triggers and GitHub credentials securely managed.

### Task 1 – Docker Builds in Jenkins

Next, I extended the Jenkins pipeline to build and push Docker images of the Django messaging app. This ensured that every pipeline run could produce a deployable container, with logs confirming successful pushes to Docker Hub.

### Task 2 – GitHub Actions for Testing

I then shifted focus to GitHub Actions, creating a `ci.yml` workflow that spins up a MySQL service, installs dependencies, and runs Django tests on every push and pull request. This brought automated testing directly into the GitHub ecosystem.

### Task 3 – Code Quality & Coverage

To enforce standards, I added linting and coverage checks to the workflow. Initially using Flake8, I later adopted Ruff for speed and Python 3.12 awareness. The workflow now fails early on lint errors, enforces single‑quote style, and uploads coverage reports as artifacts.

### Task 4 – Docker Image Deployment via GitHub Actions

Finally, I created a `dep.yml` workflow dedicated to building and pushing Docker images from the `messaging_app/` directory. Using GitHub Actions secrets for Docker Hub credentials, the pipeline securely publishes images tagged as `latest` (and optionally versioned), completing the CI/CD loop.