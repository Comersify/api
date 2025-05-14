# Order API Documentation

## Customer Order Operations

### Get My Orders
```http
GET /my-orders/
```

Get list of orders for the authenticated customer.

**Response:**
```json
{
    "type": "success",
    "data": [
        {
            "id": "number",
            "product__title": "string",
            "quantity": "number",
            "price": "number",
            "status": "string",
            "created_at": "datetime"
        }
    ]
}
```

### Create Order
```http
POST /order/create/
```

Create a new order from cart items.

**Request Body:**
```json
{
    "address": "string",
    "phoneNumber": "string",
    "postalCode": "string",
    "shippingID": "number"
}
```

**Response:**
```json
{
    "type": "success",
    "message": "Your order was submitted wait the seller to ship it"
}
```

### Create Order for Individual Seller
```http
POST /one-seller/order/create/
```

Create a direct order with an individual seller.

**Request Body:**
```json
{
    "fullName": "string",
    "quantity": "number",
    "productID": "number",
    "address": "string",
    "phoneNumber": "string",
    "postalCode": "string",
    "shippingID": "number"
}
```

**Response:**
```json
{
    "type": "success",
    "message": "Order Created"
}
```

## Vendor Order Operations

### Get Vendor Orders
```http
GET /vendor/orders/
```

Get list of orders for the vendor's products.

**Response:**
```json
{
    "type": "success",
    "data": [
        {
            "id": "number",
            "product": {
                "id": "number",
                "title": "string",
                "price": "number"
            },
            "quantity": "number",
            "status": "string",
            "shipping_info": {
                "address": "string",
                "phone_number": "string",
                "postal_code": "string"
            },
            "created_at": "datetime"
        }
    ]
}
```

### Update Order Status (Vendor Only)
```http
PUT /vendor/orders/
```

Update the status of an order.

**Request Body:**
```json
{
    "order_id": "number",
    "status": "string"
}
```

### Get Orders Analytics
```http
GET /vendor/analytics/orders/
```

Get order statistics for vendor analytics.

**Response:**
```json
{
    "type": "success",
    "data": {
        "labels": ["string"],
        "data": ["number"]
    }
}
```

## Order Status Values

Orders can have the following status values:
- `IN_CART` - Item is in shopping cart
- `SUBMITTED` - Order has been placed
- `SHIPPED` - Order has been shipped
- `DELIVERED` - Order has been delivered

## Error Responses

All endpoints may return the following error response:

```json
{
    "type": "error",
    "message": "Error description"
}
```

Common error messages include:
- "Please enter all needed information"
- "No orders found"
- "Something went wrong try later"
- "User not valid"

## Authentication

All order operations require authentication:

```http
Authorization: Bearer <access_token>
```

## Notes

1. Customer orders are created from cart items or directly with individual sellers
2. Shipping information is saved and can be reused for future orders
3. Vendors can only view and manage orders for their own products
4. Order analytics are only available for vendor accounts 