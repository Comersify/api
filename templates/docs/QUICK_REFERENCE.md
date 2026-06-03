# Comersify API Quick Reference

## Endpoints Summary

### Authentication
```
POST /signup/                      → Create account
POST /signup/{provider}/           → Google sign up
POST /login/                       → Login
POST /refresh-token/               → Refresh JWT
POST /reset-password/              → Reset password
```

### User & Settings
```
GET  /settings/                    → Get user settings
POST /settings/update/            → Update settings
GET  /store/{id}/                  → Get store info
GET  /stores/top/                  → Get top stores
GET  /customers/                   → List customers (vendor)
```

### Products
```
GET  /v2/products/                 → List products
POST /v2/products/                 → Create product
GET  /v2/products/{id}/            → Get product
PUT  /v2/products/{id}/           → Update product
DELETE /v2/products/{id}/          → Delete product
GET  /products/id/{id}/            → Product details
GET  /products/super-deals/        → Deal products
```

### Categories & Attributes
```
GET  /v2/categories/                → List categories
POST /v2/categories/               → Create category
GET  /categories/top/              → Hot categories
GET  /v2/attributes/                → List attributes
POST /v2/attributes/               → Create attribute
GET  /v2/attribute-values/          → List values
POST /v2/attribute-values/         → Create value
GET  /v2/variants/                 → List variants
POST /v2/variants/                 → Create variant
```

### Reviews
```
GET  /reviews/{product_id}         → Get reviews
```

### Cart
```
GET  /cart/products/               → Get cart
POST /cart/add-product/            → Add to cart
POST /cart/delete-product/         → Remove from cart
POST /cart/update-product/         → Update quantity
POST /cart/apply-coupon/           → Apply coupon
```

### Orders
```
GET  /my-orders/                   → Customer orders
POST /order/create/                → Create order
POST /one-seller/order/create/     → Direct order
GET  /vendor/orders/               → Vendor orders
PUT  /vendor/orders/               → Update status
GET  /vendor/analytics/orders/      → Order stats
```

### Wishlist
```
GET  /wish-list/products/          → Get wishlist
GET  /wish-list/has-product/{id}/  → Check item
POST /wish-list/add-product/       → Add item
POST /wish-list/delete-product/   → Remove item
```

### Vendor Dashboard
```
GET  /dashboard/                   → Dashboard data
GET  /vendor/products/             → Vendor products
GET  /vendor/coupons/             → List coupons
POST /vendor/coupons/             → Create coupon
GET  /vendor/discounts/           → List discounts
POST /vendor/discounts/           → Create discount
```

### Tracking
```
GET  /tracking/visits/             → Visit stats
GET  /tracking/behavior/           → User behavior
```

### Other
```
GET  /ads/                        → Get ads
GET  /site/                       → Website info
```

---

## Common Headers

```
Authorization: Bearer <token>
Content-Type: application/json
X-COMERCIFY-VISITOR: <tracker_id>
Origin: https://domain.com
```

---

## Response Format

```json
// Success
{"type": "success", "data": {...}}

// Error  
{"type": "error", "message": "..."}
```

---

## Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK |
| 201 | Created |
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

---

## URL Patterns

- Public: `/v2/products/`, `/ads/`, `/login/`
- Auth: `/cart/`, `/wish-list/`, `/my-orders/`
- Vendor: `/vendor/`, `/dashboard/`
- Admin: `/admin/`

---

## Example Requests

```bash
# Login
curl -X POST /login/ -d '{"username":"email@x.com","password":"pass"}'

# Get products
curl /v2/products/

# Add to cart
curl -X POST /cart/add-product/ \
  -H "Authorization: Bearer <token>" \
  -d '{"product_id": 123}'
```

---

## Product CRUD

```
POST   /v2/products/           → Create
GET    /v2/products/           → List
GET    /v2/products/{id}/      → Read
PUT    /v2/products/{id}/      → Update
DELETE /v2/products/{id}/      → Delete
```

## Order Flow

```
Cart → Checkout → Order Created → Vendor Ships → Delivered
```

## User Types

- `CUSTOMER` - Regular buyer
- `INDIVIDUAL-SELLER` - Single vendor
- `STORE-OWNER` - Multi-store owner
- `ADMIN` - Platform admin