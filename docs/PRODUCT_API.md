# Product API Documentation

## Product Management

### List Products
```http
GET /v2/products/
```

Get list of all products.

**Query Parameters:**
- `page`: Page number for pagination
- `category`: Filter by category ID
- `search`: Search term

### Get Product Details
```http
GET /products/id/{id}/
```

Get detailed information about a specific product.

### Create Product (Vendor Only)
```http
POST /v2/products/
```

Create a new product.

**Request Body:**
```json
{
    "title": "string",
    "description": "string",
    "price": "number",
    "buy_price": "number",
    "in_stock": "number",
    "category": "number",
    "attributes": [
        {
            "attribute": "number",
            "values": ["number"]
        }
    ]
}
```

### Update Product (Vendor Only)
```http
PUT /v2/products/{id}/
```

Update an existing product.

### Delete Product (Vendor Only)
```http
DELETE /v2/products/{id}/
```

Delete a product.

## Categories

### List Categories
```http
GET /v2/categories/
```

Get list of all categories.

### Get Hot Categories
```http
GET /categories/top/
```

Get list of popular categories.

### Create Category (Vendor Only)
```http
POST /v2/categories/
```

Create a new category.

**Request Body:**
```json
{
    "name": "string",
    "parent": "number (optional)"
}
```

## Product Variants

### List Variants
```http
GET /v2/variants/
```

Get list of product variants.

### Create Variant (Vendor Only)
```http
POST /v2/variants/
```

Create a new product variant.

**Request Body:**
```json
{
    "product": "number",
    "attributes": ["number"]
}
```

## Attributes

### List Attributes
```http
GET /v2/attributes/
```

Get list of all attributes.

### Create Attribute (Vendor Only)
```http
POST /v2/attributes/
```

Create a new attribute.

**Request Body:**
```json
{
    "name": "string"
}
```

## Attribute Values

### List Attribute Values
```http
GET /v2/attribute-values/
```

Get list of attribute values.

### Create Attribute Value (Vendor Only)
```http
POST /v2/attribute-values/
```

Create a new attribute value.

**Request Body:**
```json
{
    "attribute": "number",
    "value": "string"
}
```

## Reviews

### Get Product Reviews
```http
GET /reviews/{id}
```

Get reviews for a specific product.

## Special Offers

### Get Super Deals
```http
GET /products/super-deals/
```

Get list of products with special deals/discounts.

## Vendor Dashboard

### Get Dashboard Data
```http
GET /dashboard/
```

Get vendor dashboard statistics (vendor only).

### Manage Vendor Products
```http
GET /vendor/products/
POST /vendor/products/
GET /vendor/products/{id}
PUT /vendor/products/{id}
DELETE /vendor/products/{id}
```

Endpoints for vendors to manage their products.

## Coupons and Discounts

### Manage Coupons
```http
GET /vendor/coupons/
POST /vendor/coupons/
```

Manage product coupons (vendor only).

**Create Coupon Request Body:**
```json
{
    "product": "number",
    "code": "string",
    "value": "number",
    "end_date": "datetime"
}
```

### Manage Discounts
```http
GET /vendor/discounts/
POST /vendor/discounts/
```

Manage product discounts (vendor only).

**Create Discount Request Body:**
```json
{
    "product": "number",
    "discounted_price": "number",
    "end_date": "datetime"
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

All vendor-specific endpoints require authentication with a vendor account:

```http
Authorization: Bearer <access_token>
``` 