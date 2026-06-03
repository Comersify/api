# Cart API Documentation

## Shopping Cart Operations

### Get Cart Details
```http
GET /cart/products/
```

Get current user's shopping cart contents.

**Response:**
```json
{
    "type": "success",
    "data": {
        "orders": [
            {
                "id": "number",
                "product": {
                    "id": "number",
                    "title": "string",
                    "price": "number",
                    "image": "string"
                },
                "quantity": "number",
                "coupon": {
                    "code": "string",
                    "value": "number"
                }
            }
        ],
        "total": "number"
    }
}
```

### Add Product to Cart
```http
POST /cart/add-product/
```

Add a product to the shopping cart.

**Request Body:**
```json
{
    "product_id": "number"
}
```

**Response:**
```json
{
    "type": "success",
    "message": "Product added to cart"
}
```

### Delete Product from Cart
```http
POST /cart/delete-product/
```

Remove a product from the shopping cart.

**Request Body:**
```json
{
    "order_id": "number"
}
```

**Response:**
```json
{
    "type": "success",
    "message": "Product deleted from your cart"
}
```

### Update Product Quantity
```http
POST /cart/update-product/
```

Update the quantity of a product in the cart.

**Request Body:**
```json
{
    "order_id": "number",
    "quantity": "number"
}
```

**Response:**
```json
{
    "type": "success",
    "message": "Product quantity updated"
}
```

### Apply Coupon
```http
POST /cart/apply-coupon/
```

Apply a coupon code to a product in the cart.

**Request Body:**
```json
{
    "code": "string"
}
```

**Response:**
```json
{
    "type": "success",
    "data": {
        "coupon__code": "string",
        "coupon__value": "number",
        "product__price": "number"
    }
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

Common error messages include:
- "Data is missing"
- "Product does not exist"
- "Product already in cart"
- "Cart doesn't exist"
- "Order doesn't exist"
- "This coupon already used"
- "Coupon not valid"


## Notes

1. Products in cart are stored as orders with status "IN_CART"
2. Coupons are product-specific and can only be applied to eligible products
3. A product can only be added to the cart once (quantity can be updated instead)
4. Cart operations are only available for users with type "CUSTOMER" 