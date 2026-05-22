# FastAPI Full Auth System

A complete FastAPI authentication system with JWT, refresh tokens, role-based access, background tasks, migrations, and testing.

---

## Setup

### Create Virtual Environment
```bash
python -m venv venv
### activate 
venv\Scripts\activate
### Install Requirements
pip install -r requirements.txt
### create env file
SECRET_KEY=your_secret
DATABASE_URL=your_db_url

### Run Migrations
alembic upgrade head

### Run Server
uvicorn app.main:app --reload
##Testing
##Run tests:

pytest -v

#Run coverage:
pytest --cov=app

# Features
# JWT Authentication
# Refresh Tokens
# Role-Based Access Control (RBAC)
# Forgot Password OTP (Background Tasks)
# User Management
# Posts CRUD System
# Middleware (Logging / Request Handling)
# Alembic Migrations
# Pytest Testing
# CI/CD Ready Structure
