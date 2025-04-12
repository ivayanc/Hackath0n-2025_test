# PickME

This project is a PICKME

[STABLE VERSION](https://pick-m3-30c9736c722b.herokuapp.com/)

## Features

COMMON U DONT NEED THIS, JUST PICKME


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
