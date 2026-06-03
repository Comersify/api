# Wishlist API Documentation

## Overview

The Wishlist API allows users to save products they want to purchase later. It's a user-specific feature that persists across sessions.

## Get Wishlist Items

### Request
```http
GET /wish-list/products/
Authorization: Bearer <access_token>
```

### Response
```json
{
    "type": "success",
    "data": {
        "wishlists": [
            {
                "id": "number",
                "product": {
                    "id": "number",
                    "title": "string",
                    "price": "number",
                    "image": "string (URL)",
                    "description": "string"
                },
                "created_at": "datetime"
            }
        ],
        "count": "number"
    }
}
```

### Example Response
```json
{
    "type": "success",
    "data": {
        "wishlists": [
            {
                "id": 1,
                "product": {
                    "id": 42,
                    "title": "Premium Headphones",
                    "price": 199.99,
                    "image": "https://cdn.comersify.com/products/headphones.jpg"
                },
                "created_at": "2024-01-15T10:30:00Z"
            }
        ],
        "count": 1
    }
}
```

---

## Check Product in Wishlist

### Request
```http
GET /wish-list/has-product/<product_id>/
Authorization: Bearer <access_token>
```

### Response (Product in Wishlist)
```json
{
    "type": "success",
    "inWishList": true
}
```

### Response (Product Not in Wishlist)
```json
{
    "type": "success",
    "inWishList": false
}
```

---

## Add Product to Wishlist

### Request
```http
POST /wish-list/add-product/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "product_id": "number"
}
```

### Response
```json
{
    "type": "success",
    "message": "Product added to wishlist"
}
```

### Example Request
```bash
curl -X POST https://api.comersify.com/wish-list/add-product/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 42}'
```

---

## Remove Product from Wishlist

### Request
```http
POST /wish-list/delete-product/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "product_id": "number"
}
```

### Response
```json
{
    "type": "success",
    "message": "Product removed from wishlist"
}
```

### Example Request
```bash
curl -X POST https://api.comersify.com/wish-list/delete-product/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 42}'
```

---

## Error Responses

```json
{
    "type": "error",
    "message": "Error description"
}
```

### Common Error Messages

| Error | Description |
|-------|-------------|
| `Product not found` | Product with given ID doesn't exist |
| `Product already in wishlist` | Product was already added |
| `Product not in wishlist` | Tried to remove non-existent item |
| `Authentication required` | No valid token provided |

---

## Authentication

All wishlist endpoints require authentication:

```http
Authorization: Bearer <access_token>
```

---

## Implementation Examples

### JavaScript - Add to Wishlist
```javascript
async function addToWishlist(productId) {
    const response = await fetch('/wish-list/add-product/', {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ product_id: productId })
    });
    
    const data = await response.json();
    if (data.type === 'success') {
        updateWishlistIcon(true);
        showNotification('Added to wishlist!');
    }
}
```

### React Component
```jsx
const WishlistButton = ({ productId, isInWishlist }) => {
    const handleClick = async () => {
        const endpoint = isInWishlist 
            ? '/wish-list/delete-product/' 
            : '/wish-list/add-product/';
        
        await fetch(endpoint, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ product_id: productId })
        });
        
        // Refresh component to show updated state
    };

    return (
        <button onClick={handleClick}>
            {isInWishlist ? '❤️' : '🤍'}
        </button>
    );
};
```

---

## Notes

1. **User-specific** - Wishlist is tied to authenticated user
2. **No duplicates** - Adding same product twice doesn't create duplicates
3. **Cascade delete** - Removing product from platform also removes from wishlists
4. **Real-time sync** - Changes reflect immediately across devices

---

## Related Documentation

- [Product API](PRODUCT_API.md) - Product details and management
- [USER_API.md](USER_API.md) - User authentication