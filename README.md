# Mini_ecommerce api




## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies](#technologies)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Authentication](#authentication)
- [Running Tests](#running-tests)




## Introduction

This project is a mini e-commerce REST API built with Python, Django, and Django REST Framework. It was created as a portfolio project for a Junior Backend Developer position.
The project consists of four applications: Products, Users, Cart, and Orders, each responsible for a different part of the system. PostgreSQL is used as the database, and Docker is included to simplify development and deployment.


![alt text](<Screenshot.png>)


## Features

- JWT authentication using access and refresh tokens
- User registration and login
- Product listing and detail endpoints
- Admin-only product management (create, update, delete)
- Shopping cart management
- Order checkout
- Order history
- API documentation with Swagger and ReDoc
- Docker support

## Technologies
- Python
- Django
- Django REST Framework
- PostgreSQL
- JWT Authentication
- drf-spectacular
- Docker


## Project structure

```
.
├── Dockerfile
├── README.md
├── cart
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── docker-compose-prod.yml
├── docker-compose.yml
├── manage.py
├── media
│   └── products
├── mini_ecommerce
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
|
├── orders
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── products
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── tests.py
│   ├── urls.py
│   └── views.py
├── requirements.txt
└── users
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── serializer.py
    ├── tests.py
    ├── urls.py
    └── views.py
```

## Installation


### 1. Clone the repository

```bash
git clone https://github.com/amirpazhuhan/ecommerce_api.git
cd ecommerce_api
```

### 2. Create and activate a virtual environment

**Linux/macOS**

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows**

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create the environment variables

Create a `.env` file in the project root and add the required environment variables.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=ecommerce
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

ACCESS_TOKEN_LIFETIME=5
REFRESH_TOKEN_LIFETIME=1
```


#### Environment Variables

Copy the example environment file:

```bash
cp .env.example .env
```

Then update the values in `.env` according to your local environment.

### 5. Apply database migrations

```bash
python manage.py migrate
```

### 6. Create a superuser (optional)

```bash
python manage.py createsuperuser
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

```
http://127.0.0.1:8000/
```


## Running with Docker

Build and start the containers:

```bash
docker compose up --build
```

Run database migrations:

```bash
docker compose exec web python manage.py migrate
```

Create a superuser:

```bash
docker compose exec web python manage.py createsuperuser
```


## Authentication

This project uses JWT authentication.

After registering or logging in, users receive:

- **Access Token** – Used to authenticate requests to protected endpoints.
- **Refresh Token** – Used to obtain a new access token when the current one expires.

Include the access token in the `Authorization` header:

```http
Authorization: Bearer <access_token>
```

## Running Tests

Run all tests:

```bash
python manage.py test
```

Run tests for a specific application:

```bash
python manage.py test products
python manage.py test users
python manage.py test cart
python manage.py test orders
```


## API Documentation

After running the project, the API documentation is available at:

- Swagger UI: `/api/schema/swagger-ui/`
- ReDoc: `/api/schema/redoc/`
