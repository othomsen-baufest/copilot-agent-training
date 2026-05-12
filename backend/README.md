# JWT Authentication Backend

A minimal **FastAPI** service that issues and refreshes **JWT** tokens.  
Dependency management is handled with **Poetry**.

---

## Features

| Endpoint | Method | Description |
|---|---|---|
| `/auth/token` | POST | Authenticate and obtain an access token + refresh token |
| `/auth/token/refresh` | POST | Exchange a refresh token for a new token pair |
| `/health` | GET | Health check |
| `/docs` | GET | Interactive Swagger UI |
| `/redoc` | GET | ReDoc documentation |

- Access token expires in **300 seconds**.
- Refresh token expires in **3600 seconds**.

---

## Prerequisites

- [Python 3.11+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [Docker](https://docs.docker.com/get-docker/) *(optional)*
- [Docker Compose](https://docs.docker.com/compose/install/) *(optional)*

---

## Local Development

### 1. Install dependencies

```bash
cd backend
poetry install
```

### 2. Run the server

```bash
poetry run uvicorn app.main:app --reload
```

The API will be available at <http://localhost:8000>.

---

## Running with Docker

### Build and start

```bash
cd backend
docker compose up --build
```

### Stop

```bash
docker compose down
```

---

## Usage

### Obtain a token

```bash
curl -X POST http://localhost:8000/auth/token \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

**Response:**

```json
{
  "access_token": "<JWT>",
  "refresh_token": "<JWT>",
  "token_type": "bearer",
  "expires_in": 300
}
```

### Refresh a token

```bash
curl -X POST http://localhost:8000/auth/token/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<your_refresh_token>"}'
```

**Response:**

```json
{
  "access_token": "<new_JWT>",
  "refresh_token": "<new_JWT>",
  "token_type": "bearer",
  "expires_in": 300
}
```

---

## Testing

```bash
poetry run pytest
```

---

## Project Structure

```
backend/
├── app/
│   ├── main.py              # FastAPI application entry point
│   ├── auth/
│   │   ├── jwt_handler.py   # JWT creation, validation and user authentication
│   │   └── models.py        # Pydantic request/response models
│   └── routes/
│       └── auth.py          # /auth/token and /auth/token/refresh routes
├── tests/
│   └── test_auth.py         # Unit tests
├── pyproject.toml           # Poetry project & dependency configuration
├── Dockerfile               # Container image definition
├── docker-compose.yml       # Multi-container orchestration
└── README.md                # This file
```

---

## Configuration

The following constants in `app/auth/jwt_handler.py` can be adjusted:

| Variable | Default | Description |
|---|---|---|
| `SECRET_KEY` | `supersecretkey_change_in_production` | HMAC signing secret (use a strong random value in production) |
| `ALGORITHM` | `HS256` | JWT signing algorithm |
| `ACCESS_TOKEN_EXPIRE_SECONDS` | `300` | Access token lifetime in seconds |
| `REFRESH_TOKEN_EXPIRE_SECONDS` | `3600` | Refresh token lifetime in seconds |

> **Warning:** Always replace `SECRET_KEY` with a cryptographically secure random string before deploying to production.
