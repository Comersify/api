# Website API Documentation

## Multi-Tenant Website Management

The Website API allows vendors to manage their own storefronts with custom domains. Each vendor can have their own branded website with unique domain and styling.

## Website Model

Each website has the following properties:
```json
{
    "user": "number (vendor ID)",
    "domain": "string (main domain)",
    "test_domain": "string (development domain)",
    "logo": "string (optional)",
    "title": "string"
}
```

## Domain Handling

The API uses subdomain middleware to route requests to the appropriate vendor's store. When a request comes in:

1. The middleware extracts the domain from the request
2. It looks up the website associated with that domain
3. The request is processed in the context of that vendor's store

## Headers

All requests should include the origin domain:

```http
Origin: https://your-store-domain.com
```

## Authentication

Website management endpoints require vendor authentication:

```http
Authorization: Bearer <access_token>
```

## Notes

1. Only users with type `INDIVIDUAL-SELLER` or `STORE-OWNER` can have websites
2. Each domain must be unique across the platform
3. Test domains are provided for development purposes
4. All product and order operations are scoped to the website's vendor

## Error Responses

All endpoints may return the following error response:

```json
{
    "type": "error",
    "message": "Error description"
}
```

## Best Practices

1. Use HTTPS for all domains
2. Set up proper DNS records for domains
3. Use test domains for development and testing
4. Keep logos optimized for web use 