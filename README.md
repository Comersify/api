# E-Commerce API Documentation

This is a comprehensive e-commerce API built with Django REST Framework that supports multi-tenant architecture, allowing both individual sellers and store owners to manage their products and orders.

## Table of Contents
- [Setup](#setup)
- [Authentication](#authentication)
- [API Modules](#api-modules)
- [Environment Variables](#environment-variables)

## Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (see [Environment Variables](#environment-variables) section)

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_token>
```

## API Modules

- [User API](docs/USER_API.md) - User management, authentication, and profiles
- [Product API](docs/PRODUCT_API.md) - Product management, categories, and variants
- [Cart API](docs/CART_API.md) - Shopping cart operations
- [Order API](docs/ORDER_API.md) - Order management and tracking
- [Website API](docs/WEBSITE_API.md) - Multi-tenant website management
- [Tracking API](docs/TRACKING_API.md) - Analytics and visit tracking

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
SECRET_KEY=your_secret_key
DEBUG=True

# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_STORAGE_BUCKET_NAME=your_bucket_name
AWS_S3_REGION_NAME=your_region

# Database Configuration
PGDATABASE=your_db_name
PGUSER=your_db_user
PGPASSWORD=your_db_password
PGHOST=your_db_host
PGPORT=your_db_port
```

## User Types

The API supports different user types with varying permissions:

- `ADMIN` - Full system access
- `CUSTOMER` - Can browse products, make orders
- `VENDOR` - Can manage products and fulfill orders
- `INDIVIDUAL-SELLER` - Can sell products individually
- `STORE-OWNER` - Can manage a full store with multiple products

## Error Handling

All API endpoints return responses in the following format:

```json
{
    "type": "success|error",
    "message": "Description of the result",
    "data": {} // Optional data object
}
``` 