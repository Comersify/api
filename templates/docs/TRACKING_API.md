# Tracking API Documentation

## Overview

The Tracking API provides analytics and visitor tracking functionality for the e-commerce platform. It tracks user behavior, page visits, and provides analytics data for vendors.

## Tracking Headers

All requests should include the following headers for proper tracking:

```http
X-COMERCIFY-VISITOR: <tracker_id>
Origin: <client_domain>
User-Agent: <browser_info>
```

## Tracking Model

Each visit is tracked with the following information:
```json
{
    "tracker_id": "string (UUID)",
    "client_url": "string",
    "client_path": "string",
    "api_path": "string",
    "browser": "string",
    "sub_domain": "number (website ID)",
    "ip_address": "string",
    "logged_in": "boolean"
}
```

## Tracking Process

1. When a user first visits the site, they are assigned a unique `tracker_id`
2. All subsequent requests include this ID in the `X-COMERCIFY-VISITOR` header
3. The tracking middleware logs each API request
4. Visits are associated with users when they are logged in

## Analytics Data

### Visit Analytics
```http
GET /tracking/visits/
```

Get visit statistics for a vendor's store.

**Response:**
```json
{
    "type": "success",
    "data": {
        "total_visits": "number",
        "unique_visitors": "number",
        "logged_in_visits": "number",
        "visit_by_page": {
            "page_path": "number"
        }
    }
}
```

### User Behavior
```http
GET /tracking/behavior/
```

Get user behavior analytics.

**Response:**
```json
{
    "type": "success",
    "data": {
        "most_viewed_products": [
            {
                "product_id": "number",
                "views": "number"
            }
        ],
        "conversion_rate": "number",
        "average_session_duration": "number"
    }
}
```

## Privacy Considerations

1. IP addresses are stored but not exposed through the API
2. User tracking IDs are randomly generated UUIDs
3. Personal information is only associated when users are logged in
4. Tracking data is scoped to individual vendor stores

## Error Responses

All endpoints may return the following error response:

```json
{
    "type": "error",
    "message": "Error description"
}
```

## Authentication

Analytics endpoints require vendor authentication:

```http
Authorization: Bearer <access_token>
```

## Notes

1. Tracking is automatic through middleware
2. Analytics data is only available to vendors for their own stores
3. Historical data is retained according to platform policies
4. Real-time tracking updates may have slight delays 