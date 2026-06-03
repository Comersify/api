# Comersify API Documentation

Welcome to the Comersify API documentation. This comprehensive guide covers all available endpoints for the Comersify e-commerce platform.

## 📚 Documentation Index

### Core APIs
| Document | Description |
|----------|-------------|
| [USER_API.md](USER_API.md) | Authentication, user accounts, store management |
| [PRODUCT_API.md](PRODUCT_API.md) | Products, categories, variants, reviews, coupons |
| [ORDER_API.md](ORDER_API.md) | Customer and vendor order management |
| [CART_API.md](CART_API.md) | Shopping cart operations |
| [WISHLIST_API.md](WISHLIST_API.md) | User wishlist management |
| [TRACKING_API.md](TRACKING_API.md) | Visitor tracking and analytics |
| [ADS_API.md](ADS_API.md) | Promotional content and ads |
| [WEBSITE_API.md](WEBSITE_API.md) | Multi-tenant website management |

---

## Quick Start

### 1. Authentication
```bash
# Sign up
curl -X POST https://api.comersify.com/signup/ \
  -H "Content-Type: application/json" \
  -d '{"firstName":"John","lastName":"Doe","email":"john@example.com","password":"secret123","phoneNumber":"+1234567890"}'

# Login
curl -X POST https://api.comersify.com/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"john@example.com","password":"secret123"}'
```

### 2. Browse Products
```bash
curl https://api.comersify.com/v2/products/
```

### 3. Manage Cart
```bash
# Add to cart
curl -X POST https://api.comersify.com/cart/add-product/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"product_id": 123}'
```

---

## Base URL

```
Production: https://api.comersify.com
Development: http://localhost:8000
```

## Authentication

All authenticated endpoints require a JWT token:

```http
Authorization: Bearer <access_token>
```

## Response Format

**Success:**
```json
{
    "type": "success",
    "data": { ... },
    "message": "Optional message"
}
```

**Error:**
```json
{
    "type": "error",
    "message": "Error description"
}
```

---

## API Reference by Category

### 👤 Authentication & Users
| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/signup/` | POST | Create account | No |
| `/login/` | POST | Login | No |
| `/refresh-token/` | POST | Refresh JWT | No |
| `/settings/` | GET | User settings | Yes |
| `/settings/update/` | POST | Update settings | Yes |
| `/store/{id}/` | GET | Store details | No |
| `/stores/top/` | GET | Top stores | No |

### 📦 Products & Catalog
| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/v2/products/` | GET | List products | No |
| `/v2/products/` | POST | Create product | Vendor |
| `/products/id/{id}/` | GET | Product details | No |
| `/products/super-deals/` | GET | Deal products | No |
| `/v2/categories/` | GET/POST | Categories | Both |
| `/v2/attributes/` | GET/POST | Attributes | Vendor |
| `/reviews/{id}` | GET | Product reviews | No |
| `/vendor/coupons/` | GET/POST | Coupons | Vendor |

### 🛒 Orders & Cart
| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/cart/products/` | GET | View cart | Yes |
| `/cart/add-product/` | POST | Add to cart | Yes |
| `/cart/update-product/` | POST | Update quantity | Yes |
| `/cart/apply-coupon/` | POST | Apply coupon | Yes |
| `/my-orders/` | GET | Customer orders | Yes |
| `/order/create/` | POST | Create order | Yes |
| `/vendor/orders/` | GET | Vendor orders | Vendor |
| `/vendor/analytics/orders/` | GET | Order stats | Vendor |

### ❤️ Wishlist
| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/wish-list/products/` | GET | Get wishlist | Yes |
| `/wish-list/has-product/{id}/` | GET | Check item | Yes |
| `/wish-list/add-product/` | POST | Add item | Yes |
| `/wish-list/delete-product/` | POST | Remove item | Yes |

### 📊 Analytics & Tracking
| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/tracking/visits/` | GET | Visit stats | Vendor |
| `/tracking/behavior/` | GET | User behavior | Vendor |

### 📢 Advertising
| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/ads/` | GET | Get active ads | No |

### 🌐 Websites
| Endpoint | Method | Description | Auth |
|----------|--------|-------------|------|
| `/site/` | GET | Website info | Yes |

---

## Admin Dashboard

Access the admin dashboard at: **`/admin/`**

Features:
- 🎨 Modern shadcn/ui design
- 🌙 Dark mode toggle
- 📱 Responsive layout
- ⚡ Quick actions panel
- 📈 System status indicators

---

## API Versioning

Current version: **v2**

All v2 endpoints are prefixed with `/v2/`:
- `/v2/products/`
- `/v2/categories/`
- `/v2/attributes/`
- `/v2/attribute-values/`
- `/v2/variants/`

---

## Rate Limiting

| Tier | Requests/Hour |
|------|-------------|
| Anonymous | 100 |
| Authenticated | 1000 |
| Vendor | 5000 |

---

## Error Codes

| Code | Meaning |
|------|---------|
| 400 | Bad Request |
| 401 | Unauthorized |
| 403 | Forbidden |
| 404 | Not Found |
| 500 | Server Error |

---

## SDKs & Libraries

- **Python (Django)**: Native REST API
- **JavaScript**: Use native `fetch` or Axios
- **React Native**: REST client integration

---

## Support

📧 Email: api-support@comersify.com  
🐙 GitHub: https://github.com/Comersify/api  
📖 Docs: https://docs.comersify.com