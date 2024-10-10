# Inventory Management System API
Project Overview
This project is a Backend API for a Simple Inventory Management System built using Django Rest Framework (DRF). The system supports basic CRUD operations on inventory items, integrated with JWT-based authentication for secure access. Redis is used to cache frequently accessed inventory data to improve performance, and PostgreSQL is the main database for storing inventory items.

This API does not have any frontend pages and is designed to be consumed by other applications or systems that need to manage inventory.

Technologies Used
Django - Python-based web framework for building the backend.
Django Rest Framework (DRF) - A powerful toolkit for building Web APIs.
PostgreSQL - Relational database management system.
Redis - In-memory data structure store, used as a cache.
JWT (JSON Web Token) - For securing API endpoints.
Django REST Framework SimpleJWT - Provides JWT-based authentication.
Logging - To capture API usage, errors, and significant events.

# Setup Instructions
1. Prerequisites
Make sure you have the following installed:
Python 3.x
PostgreSQL
Redis

2. Configure PostgreSQL
Ensure PostgreSQL is installed and running. Create a database and user for the project:
# In PostgreSQL shell
CREATE DATABASE inventory_db;

3. Configure Redis
Ensure Redis is installed and running locally.

4. Run Migrations
Apply the database migrations to create the necessary tables.

python manage.py makemigrations
python manage.py migrate

5. Run the Development Server
Start the Django development server:
python manage.py runserver
Your API should now be running at http://127.0.0.1:8000/.

6. Running Tests
To ensure everything works, run the provided unit tests:

python manage.py test inventory

API Documentation
Authentication Endpoints
# User Registration
POST /inventory/api/register/
Request Body:
{
    "username": "new_user",
    "email": "user@example.com",
    "password": "securepassword"
}
Response:
{
    "username": "new_user",
    "email": "user@example.com"
}
# Login (Obtain Token)
POST /inventory/api/token/
Request Body:
{
    "username": "your_username",
    "password": "your_password"
}
Response:
{
    "access": "<JWT access token>",
    "refresh": "<JWT refresh token>"
}
# Token Refresh
POST /inventory/api/token/refresh/
Request Body:
{
    "refresh": "<JWT refresh token>"
}
Response:
{
    "access": "<new JWT access token>"
}
Inventory Endpoints
# Create Item
POST /inventory/items/
Request Body:
{
    "name": "Item name",
    "description": "Item description",
    "quantity": 100
}
Response (Success):
{
    "id": 1,
    "name": "Item name",
    "description": "Item description",
    "quantity": 100
}
Error Response (Item already exists):
{
    "error": "Item already exists"
}
# Read Item
GET /inventory/items/<item_id>/
Response (Success):
{
    "id": 1,
    "name": "Item name",
    "description": "Item description",
    "quantity": 100
}
Error Response (Item not found):
{
    "error": "Item not found"
}
# Update Item
PUT /inventory/items/<item_id>/
Request Body:
{
    "name": "Updated name",
    "description": "Updated description",
    "quantity": 150
}
Response (Success):
{
    "id": 1,
    "name": "Updated name",
    "description": "Updated description",
    "quantity": 150
}
# Delete Item
DELETE /inventory/items/<item_id>/
Response (Success):
{
    "message": "Item deleted"
}
# Caching
The Read Item endpoint (GET /items/<item_id>/) is cached using Redis.
The first request will hit the database and store the item in Redis. Subsequent requests will be served from the cache, improving performance.
Logging
The system uses Django’s logging framework to track API usage, errors, and significant events. The logs can be viewed in the console during development.

# Unit Tests
The project includes unit tests for the following scenarios:

Create Item
Read Item
Update Item
Delete Item
Authentication (registration, login)
You can run the tests using:

python manage.py test inventory
