# PickME

Test task for Hackath0n-2025

[STABLE VERSION](https://hackath0n-2025test-9e2a414779d4.herokuapp.com/docs)

## Features

AUTH0 authorization
Postgresql database

## Installation

1. Clone the repository
2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```
3. Install dependencies:
```
pip install -r requirements.txt
```
4. Set up environment variables in `.env` file (see `.env.example`)

## Database Migrations

Initialize the database with Alembic:

```
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## Running the Application

Start the FastAPI application:

```
uvicorn app.main:app --reload
```

## Authentication

This API uses Auth0 for authentication. You need to include a valid JWT token in the `Authorization` header of your requests:

```
Authorization: Bearer YOUR_AUTH0_TOKEN
```
