# REST Product Service

A RESTful Product Management API built using **Python, FastAPI, PostgreSQL, and SQLAlchemy**. This service provides product CRUD operations, pagination, filtering, sorting, database migrations, structured error handling, and automated testing.

## 1. Project Overview

The REST Product Service is designed to manage product information through REST APIs.

### Key Features

- Create a new product.
- Retrieve product details by ID.
- Retrieve all products.
- Update product information.
- Partially update product information.
- Delete products.
- Pagination support.
- Filter products by category, status, and price range.
- Sort product records.
- Input validation using Pydantic.
- Custom exception handling.
- Structured application logging.
- Database migrations using Alembic.
- Unit and integration testing.

## 2. Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.14 | Programming language |
| FastAPI | REST API framework |
| PostgreSQL | Relational database |
| SQLAlchemy | ORM and database operations |
| Alembic | Database migrations |
| Pydantic | Data validation and DTOs |
| Uvicorn | ASGI application server |
| Pytest | Automated testing |
| Pytest-Cov | Test coverage reporting |
| HTTPX | API testing |

## 3. Project Architecture

The application follows a layered architecture.

```text
Client
  |
  v
Controller Layer
  |
  v
Service Layer
  |
  v
Repository Layer
  |
  v
PostgreSQL Database
```

### Layer Responsibilities

**Controller Layer**
- Handles incoming HTTP requests.
- Defines REST API endpoints.
- Validates request and response data.

**Service Layer**
- Implements business logic.
- Handles product validation.
- Manages duplicate product checks.
- Handles product-related exceptions.

**Repository Layer**
- Performs database operations.
- Creates, retrieves, updates, and deletes products.
- Supports filtering, sorting, and pagination.

**Database Layer**
- Uses PostgreSQL for persistent data storage.
- SQLAlchemy manages database interactions.
- Alembic handles schema migrations.

## 4. Project Structure

```text
Product_Service/
│
├── app/
│   ├── controllers/
│   │   └── product_controller.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── exceptions.py
│   │   └── logging_config.py
│   │
│   ├── db/
│   │   └── session.py
│   │
│   ├── models/
│   │   └── product.py
│   │
│   ├── repositories/
│   │   └── product_repository.py
│   │
│   ├── schemas/
│   │   ├── error.py
│   │   └── product.py
│   │
│   ├── services/
│   │   └── product_service.py
│   │
│   └── main.py
│
├── alembic/
│   └── versions/
│
├── tests/
│   ├── unit/
│   │   └── test_product_service.py
│   │
│   └── integration/
│       ├── conftest.py
│       └── test_product_api.py
│
├── logs/
│
├── .env
├── .gitignore
├── alembic.ini
├── requirements.txt
└── README.md
```

## 5. Database Configuration

Database: PostgreSQL

Main database name: `product_service`

Test database name: `product_service_test`

Configure the `.env` file:

```env
APP_NAME=REST Product Service
APP_ENV=development
DEBUG=True
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/product_service
TEST_DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/product_service_test
API_V1_PREFIX=/api/v1
```

Replace `YOUR_PASSWORD` with your PostgreSQL password.

## 6. Product Database Model

The application maintains a `products` table.

| Field | Description |
|---|---|
| id | Unique product UUID |
| name | Product name |
| description | Product description |
| price | Product price |
| quantity | Available product quantity |
| category | Product category |
| status | ACTIVE or INACTIVE |
| created_at | Product creation timestamp |
| updated_at | Last update timestamp |

Database constraints ensure valid product values, including positive prices and non-negative quantities.

Product names are protected by a case-insensitive unique index.

## 7. Installation and Setup

### Prerequisites

- Python
- PostgreSQL
- pip

### Step 1: Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd Product_Service
```

### Step 2: Create virtual environment

```bash
py -m venv venv
```

### Step 3: Activate virtual environment

Windows CMD:

```cmd
venv\Scripts\activate.bat
```

### Step 4: Install dependencies

```bash
py -m pip install -r requirements.txt
```

### Step 5: Configure environment variables

Create a `.env` file and configure the PostgreSQL database URLs.

### Step 6: Run database migrations

```bash
py -m alembic upgrade head
```

### Step 7: Start the application

```bash
py -m uvicorn app.main:app --reload --port 8000
```

Application URL:

`http://127.0.0.1:8000`

## 8. API Endpoints

Base URL:

`/api/v1/products`

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/products` | Create product |
| GET | `/api/v1/products` | List products |
| GET | `/api/v1/products/{product_id}` | Get product by ID |
| PUT | `/api/v1/products/{product_id}` | Fully update product |
| PATCH | `/api/v1/products/{product_id}` | Partially update product |
| DELETE | `/api/v1/products/{product_id}` | Delete product |

### Product Listing Features

The listing endpoint supports:

- Pagination using `page` and `size`.
- Category filtering.
- Status filtering.
- Minimum price filtering.
- Maximum price filtering.
- Sorting using supported sort fields.

Example:

```http
GET /api/v1/products?page=1&size=10&category=Electronics&status=ACTIVE
```

Price filtering example:

```http
GET /api/v1/products?minPrice=100&maxPrice=1000
```

Sorting example:

```http
GET /api/v1/products?sort=name
```

Refer to the application's OpenAPI documentation for the exact supported query parameters.

## 9. API Documentation

FastAPI automatically generates interactive API documentation.

Swagger UI:

`http://127.0.0.1:8000/docs`

ReDoc:

`http://127.0.0.1:8000/redoc`

Health Check:

`http://127.0.0.1:8000/health`

## 10. Error Handling

The application implements centralized exception handling.

| HTTP Status | Description |
|---|---|
| 400 | Invalid request |
| 404 | Product not found |
| 409 | Duplicate product |
| 422 | Validation error |
| 500 | Internal server error |

Example error response:

```json
{
  "success": false,
  "message": "Product not found",
  "error": {
    "product_id": "product-uuid"
  }
}
```

## 11. Logging

Application logging is configured using Python's logging module.

- Console logging.
- File-based logging.
- INFO-level application events.
- Error and exception logging.

Log file:

`logs/app.log`

## 12. Testing

The project includes unit tests and integration tests.

### Run Unit Tests

```bash
py -m pytest tests/unit/test_product_service.py -v
```

### Run Integration Tests

```bash
py -m pytest tests/integration/test_product_api.py -v
```

### Run Unit Tests with Coverage

```bash
py -m pytest tests/unit/test_product_service.py -v --cov=app.services.product_service --cov-report=term-missing
```

### Test Results

| Test Type | Passed |
|---|---:|
| Unit Tests | 10 |
| Integration Tests | 8 |
| Total | 18 |

Service Layer Test Coverage: **82%**

## 13. Database Migration Commands

Generate a migration:

```bash
py -m alembic revision --autogenerate -m "migration_message"
```

Apply migrations:

```bash
py -m alembic upgrade head
```

Check migration history:

```bash
py -m alembic history
```

## 14. Conclusion

The REST Product Service provides a structured and maintainable backend solution for product management.

It follows layered architecture principles, uses PostgreSQL for reliable data storage, implements RESTful API standards, and includes automated testing to verify application functionality.

The project demonstrates practical implementation of FastAPI, SQLAlchemy, Alembic, database integration, exception handling, logging, and API testing.
