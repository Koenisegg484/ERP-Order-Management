# ERP Order Management System (Backend)

A production-ready **Order Management backend** built with **Django Rest Framework**, designed to demonstrate real-world backend engineering practices including authentication, async processing, inventory consistency, logging, testing, and containerization.

---

## 🚀 Features

- JWT Authentication (access & refresh tokens)
- Role-based permissions (Admin / Staff)
- Product & Inventory Management
- Order lifecycle with valid state transitions
- Inventory locking using database transactions
- Asynchronous task processing using Celery + Redis
- Pagination, filtering, ordering
- Centralized logging & error handling middleware
- Unit & API tests
- Dockerized setup (Django, Postgres, Redis, Celery)
- Swagger / OpenAPI documentation

---

## 🛠 Tech Stack

- **Backend**: Django, Django REST Framework
- **Database**: PostgreSQL
- **Auth**: JWT (SimpleJWT)
- **Async Tasks**: Celery + Redis
- **Docs**: Swagger (drf-spectacular)
- **Testing**: Django TestCase, DRF APITestCase
- **Infra**: Docker, Docker Compose

---

## 📂 Project Structure

```
ERP-Order-Management/
│
├── config/                # Core project config
│   ├── settings.py
│   ├── urls.py
│   ├── middlewares.py
│
├── products/              # Product & inventory domain
│
├── orders/                # Orders, items, history, reports
│
├── docker-compose.yml
├── Dockerfile
└── manage.py
```

---

## 🔐 Authentication Flow (JWT)

1. User logs in → receives **access + refresh token**
2. Access token is sent via:
   ```
   Authorization: Bearer <access_token>
   ```
3. When access token expires, client calls refresh endpoint
4. New access token is issued

---

## 📘 API Documentation (Swagger)

Swagger UI is enabled using **drf-spectacular**.

### Access Swagger UI

```
http://localhost:8000/api/docs/
```

### Access OpenAPI schema

```
http://localhost:8000/api/schema/
```

Swagger allows:
- Interactive API testing
- JWT authentication via UI
- Automatic schema generation

---

## 📦 Order Lifecycle

```
PENDING → CONFIRMED → SHIPPED → DELIVERED
        ↘ CANCELLED
```

- Only valid transitions are allowed
- Inventory is deducted on CONFIRMED
- Inventory is restored on CANCELLED
- All operations are wrapped in DB transactions

---

## 🔄 Asynchronous Processing

- Order creation triggers a Celery task
- Tasks are queued using Redis
- Celery is mocked in unit tests for isolation

---

## 🧪 Running Tests

### Inside Docker (Recommended)

```bash
docker-compose exec web python manage.py test
```

### Test Coverage Includes

- Models
- Serializers
- API endpoints
- Permissions
- Celery task triggering (mocked)

---

## 🐳 Running the Project

```bash
docker-compose up --build
```

Services started:
- Django API
- PostgreSQL
- Redis
- Celery worker

---

## 📊 Logging & Error Handling

- Custom exception logging middleware
- Errors logged with stack traces
- Production-friendly structure

---

## 📈 Reports Endpoint

Admins can fetch system-wide metrics:

- Total orders
- Total revenue
- Low stock alerts

---

## 🧠 Design Highlights

- Clear separation of concerns
- Database-level consistency guarantees
- Async side-effects isolated
- Testable, maintainable architecture

---

## 👨‍💻 Author Notes

This project is intentionally built to reflect **real-world backend systems**, focusing on:
- Data integrity
- Scalability
- Observability
- Clean API design

Ideal as a **portfolio project**, **interview take-home**, or **backend reference implementation**.

---

## ✅ Future Improvements

- API versioning
- Caching layer
- Rate limiting
- Frontend (React / Next.js)
- CI pipeline

