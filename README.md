# Library API

Library Service — an online management system for book borrowings, built with Django REST Framework.
It replaces paper-based tracking of books, borrowings, users and payments with a REST API
that is fully usable through the browsable API and Swagger UI.

## Current status

| Part | Status |
|------|--------|
| Users service (custom user with email login, registration, JWT, profile) | Done |
| Books service | Planned |
| Borrowings service | Planned |
| Payments | Planned |

This README is extended with every finished task.

## Tech stack

- Python 3.13
- Django 6.1
- Django REST Framework
- Simple JWT (JWT authentication)
- drf-spectacular (Swagger / OpenAPI documentation)
- python-dotenv (environment variables)
- SQLite (default database)
- black, flake8 (code style), coverage (test coverage)

## Getting started

1. Clone the repository and go to the project folder:

   ```bash
   git clone <repository-url>
   cd Library_API
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create the `.env` file from the sample and fill in your values:

   ```bash
   cp .env.sample .env
   ```

   | Variable | Description |
   |----------|-------------|
   | `SECRET_KEY` | Django secret key |
   | `DEBUG` | `True` for development, anything else disables debug |

   The `.env` file is ignored by git and must never be committed.

5. Apply migrations and run the server:

   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

6. (Optional) Create an administrator:

   ```bash
   python manage.py createsuperuser
   ```

The API is now available at `http://127.0.0.1:8000/`.

## API documentation

Interactive Swagger UI: `http://127.0.0.1:8000/api/docs/`

OpenAPI schema: `http://127.0.0.1:8000/api/schema/`

## Authentication

The project uses a custom `User` model: the **email** is the login (there is no username).

Authentication is done with JWT tokens.

> **Important:** the token is sent in the **`Authorize`** header, not in the standard `Authorization` header.
> This makes it convenient to work with browser extensions such as ModHeader.

```
Authorize: Bearer <access_token>
```

How to authenticate:

1. Register: `POST /users/`.
2. Get tokens: `POST /users/token/` with your email and password.
3. Send the `access` token in the `Authorize` header with every request to a protected endpoint.
4. When the `access` token expires, get a new one via `POST /users/token/refresh/`.

> Swagger UI: the `Authorize` header is described as a parameter on each protected endpoint,
> so paste the value `Bearer <access_token>` into that field before pressing **Execute**.

## Endpoints

### Users

| Method | URL | Auth required | Description |
|--------|-----|---------------|-------------|
| POST | `/users/` | No | Register a new user |
| POST | `/users/token/` | No | Get a pair of JWT tokens (`access`, `refresh`) |
| POST | `/users/token/refresh/` | No | Get a new `access` token using a `refresh` token |
| GET | `/users/me/` | Yes | Get the profile of the current user |
| PUT | `/users/me/` | Yes | Update the profile of the current user |
| PATCH | `/users/me/` | Yes | Partially update the profile of the current user |

#### `POST /users/` — register

Request body:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `email` | string | yes | Unique email, used as the login |
| `password` | string | yes | Password (write only, stored hashed) |

```json
{
  "email": "user@example.com",
  "password": "strongpassword123"
}
```

Response `201 Created`:

```json
{
  "email": "user@example.com"
}
```

#### `POST /users/token/` — get tokens

Request body:

```json
{
  "email": "user@example.com",
  "password": "strongpassword123"
}
```

Response `200 OK`:

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

Invalid credentials return `401 Unauthorized`.

#### `POST /users/token/refresh/` — refresh the access token

Request body:

```json
{
  "refresh": "<refresh_token>"
}
```

Response `200 OK`:

```json
{
  "access": "<new_access_token>"
}
```

#### `GET /users/me/` — my profile

Headers: `Authorize: Bearer <access_token>`

Response `200 OK`:

```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

Without a valid token the response is `401 Unauthorized`.

#### `PUT /users/me/` and `PATCH /users/me/` — update my profile

Headers: `Authorize: Bearer <access_token>`

| Field | Type | Description |
|-------|------|-------------|
| `email` | string | New email |
| `first_name` | string | First name |
| `last_name` | string | Last name |

`PUT` replaces the profile data, `PATCH` changes only the fields you send.

```json
{
  "first_name": "John",
  "last_name": "Doe"
}
```

## Tests and coverage

Run the tests:

```bash
python manage.py test
```

Run the tests with a coverage report:

```bash
coverage run manage.py test
coverage report
```

## Code style

```bash
black .
flake8
```

The flake8 settings are stored in `.flake8`.

## Project structure

```
core/            project settings and root URLs
user/            users app: custom user model, serializers, views, tests
manage.py
requirements.txt
.env.sample      example of environment variables
.flake8          flake8 configuration
```
