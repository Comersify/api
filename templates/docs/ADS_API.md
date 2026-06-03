# Ads API Documentation

## Overview

The Ads API provides access to promotional content and advertisements displayed across the platform.

## Get Active Ads

### Request
```http
GET /ads/
```

### Response
```json
{
    "type": "success",
    "data": [
        {
            "id": "number",
            "title": "string",
            "image": "string (URL)",
            "link": "string (URL)",
            "is_active": "boolean",
            "start_date": "datetime (optional)",
            "end_date": "datetime (optional)"
        }
    ]
}
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `page` | integer | Page number for pagination (optional) |
| `limit` | integer | Number of ads per page (optional) |

### Example Request
```bash
curl -X GET https://api.comersify.com/ads/?page=1&limit=10
```

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `id` | integer | Unique ad identifier |
| `title` | string | Ad title or headline |
| `image` | string | URL to ad image |
| `link` | string | URL to redirect when ad is clicked |
| `is_active` | boolean | Whether ad is currently active |
| `start_date` | datetime | When ad campaign starts (optional) |
| `end_date` | datetime | When ad campaign ends (optional) |

## Error Responses

```json
{
    "type": "error",
    "message": "Error description"
}
```

Common error messages:
- "No ads available"
- "Invalid parameters"

## Notes

1. Only active ads are returned by default
2. Ads are sorted by priority or start date
3. Expired campaigns are automatically excluded
4. Image URLs are time-limited and should be refreshed periodically

## Authentication

Authentication is not required for retrieving ads.

## Implementation

### Backend Model
The Ads model typically includes:
- Title and description
- Image URL (hosted on CDN or storage)
- Target URL for click-through
- Active status flag
- Campaign start/end dates
- Priority/position field
- Click tracking metrics

### Frontend Integration
```javascript
// Example: Fetch and display ads
async function getAds() {
    const response = await fetch('/ads/');
    const data = await response.json();
    
    if (data.type === 'success') {
        return data.data;
    }
    throw new Error(data.message);
}
```

## Best Practices

1. **Cache ads locally** - Don't fetch on every page load
2. **Handle missing images** - Show fallback for broken images
3. **Track impressions** - Log when ads are displayed
4. **Track clicks** - Log when ads are clicked
5. **Respect timing** - Don't show expired campaigns