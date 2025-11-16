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
