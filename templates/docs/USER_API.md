# User API Documentation

## Authentication Endpoints

### Sign Up
```http
POST /signup/
```

Create a new customer account.

**Request Body:**
```json
{
    "firstName": "string",
    "lastName": "string",
    "password": "string",
    "passwordConfermation": "string",
    "email": "string",
    "phoneNumber": "string"
}
```

### Sign Up with Provider (Google)
```http
POST /signup/{provider}/
```

Sign up using a third-party provider (currently supports Google).

**Request Body:**
```json
{
    "token": "string",
    "userType": "string"
}
```

### Login
```http
POST /login/
```

Login with email and password.

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Response:**
```json
{
    "type": "success",
    "name": "string",
    "image": "string (optional)"
}
```

### Refresh Token
```http
POST /refresh-token/
```

Get a new access token using refresh token.

**Request Body:**
```json
{
    "refresh": "string"
}
```

## User Settings

### Get User Settings
```http
GET /settings/
```

Get current user's settings.

**Response:**
```json
{
    "type": "success",
    "data": {
        "first_name": "string",
        "last_name": "string",
        "email": "string",
        "phone_number": "string",
        "image": "string (optional)"
    }
}
```

### Update User Settings
```http
POST /settings/update/
```

Update user settings.

**Request Body:**
```json
{
    "firstName": "string (optional)",
    "lastName": "string (optional)",
    "email": "string (optional)",
    "phoneNumber": "string (optional)",
    "oldPassword": "string (optional)",
    "password": "string (optional)",
    "passwordConfermation": "string (optional)",
    "file": "image file (optional)"
}
```

## Store Management

### Get Store Details
```http
GET /store/{id}/
```

Get store details by ID.

### Get Top Stores
```http
GET /stores/top/
```

Get list of top-performing stores.

## Customer Management

### Get Customers
```http
GET /customers/
```

Get list of customers (requires vendor/admin privileges).

## App Reviews

### Get App Reviews
```http
GET /reviews/
```

Get recent app reviews.

## Password Management

### Reset Password
```http
POST /reset-password/
```

Request password reset.

**Request Body:**
```json
{
    "email": "string"
}
```

## Error Responses

All endpoints may return the following error response:

```json
{
    "type": "error",
    "message": "Error description"
}
```

## Authentication

All endpoints except signup, login, and password reset require authentication using JWT token:

```http
Authorization: Bearer <access_token>
``` 