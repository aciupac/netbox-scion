# NetBox SCION Plugin API Documentation

This document provides comprehensive API documentation for the NetBox SCION plugin, including endpoints, request/response examples, and common usage patterns.

## Base URL

All API endpoints are prefixed with:
```
/api/plugins/scion/
```

For a NetBox instance running at `https://netbox.example.com`, the full base URL would be:
```
https://netbox.example.com/api/plugins/scion/
```

## Authentication

The API uses the same authentication methods as NetBox:

- **Token Authentication** (Recommended): Include `Authorization: Token <your-token>` header
- **Session Authentication**: For browser-based access with CSRF tokens

### Getting an API Token
1. Log into NetBox web interface
2. Go to your user profile → API Tokens
3. Create a new token with appropriate permissions

## Content Type

All requests should use JSON content type:
```
Content-Type: application/json
```

---

## 📋 Organizations API

Manage SCION network operators and organizations.

### Base Endpoint
```
/api/plugins/scion/organizations/
```

### List Organizations

**GET** `/api/plugins/scion/organizations/`

```bash
curl -X GET \
  "https://netbox.example.com/api/plugins/scion/organizations/" \
  -H "Authorization: Token your-api-token" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "url": "https://netbox.example.com/api/plugins/scion/organizations/1/",
      "display": "ACME",
      "short_name": "ACME",
      "full_name": "ACME Corporation",
      "description": "Sample SCION operator",
      "created": "2025-09-09T10:00:00.000000Z",
      "last_updated": "2025-09-09T10:00:00.000000Z",
      "custom_field_data": {}
    },
    {
      "id": 2,
      "url": "https://netbox.example.com/api/plugins/scion/organizations/2/",
      "display": "EXAMPLE",
      "short_name": "EXAMPLE",
      "full_name": "Example Networks Ltd",
      "description": "",
      "created": "2025-09-09T10:15:00.000000Z",
      "last_updated": "2025-09-09T10:15:00.000000Z",
      "custom_field_data": {}
    }
  ]
}
```

### Get Organization

**GET** `/api/plugins/scion/organizations/{id}/`

```bash
curl -X GET \
  "https://netbox.example.com/api/plugins/scion/organizations/1/" \
  -H "Authorization: Token your-api-token" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "id": 1,
  "url": "https://netbox.example.com/api/plugins/scion/organizations/1/",
  "display": "ACME",
  "short_name": "ACME",
  "full_name": "ACME Corporation",
  "description": "Sample SCION operator providing connectivity services",
  "created": "2025-09-09T10:00:00.000000Z",
  "last_updated": "2025-09-09T10:00:00.000000Z",
  "custom_field_data": {}
}
```

### Create Organization

**POST** `/api/plugins/scion/organizations/`

```bash
curl -X POST \
  "https://netbox.example.com/api/plugins/scion/organizations/" \
  -H "Authorization: Token your-api-token" \
  -H "Content-Type: application/json" \
  -d '{
    "short_name": "NEWCORP",
    "full_name": "New Corporation Inc",
    "description": "A new SCION network operator"
  }'
```

**Request Body:**
```json
{
  "short_name": "NEWCORP",
  "full_name": "New Corporation Inc", 
  "description": "A new SCION network operator"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "url": "https://netbox.example.com/api/plugins/scion/organizations/3/",
  "display": "NEWCORP",
  "short_name": "NEWCORP",
  "full_name": "New Corporation Inc",
  "description": "A new SCION network operator",
  "created": "2025-09-09T12:00:00.000000Z",
  "last_updated": "2025-09-09T12:00:00.000000Z",
  "custom_field_data": {}
}
```

### Update Organization

**PATCH** `/api/plugins/scion/organizations/{id}/`

```bash
curl -X PATCH \
  "https://netbox.example.com/api/plugins/scion/organizations/3/" \
  -H "Authorization: Token your-api-token" \
  -H "Content-Type: application/json" \
  -d '{
    "description": "Updated description for the organization"
  }'
```

### Delete Organization

**DELETE** `/api/plugins/scion/organizations/{id}/`

```bash
curl -X DELETE \
  "https://netbox.example.com/api/plugins/scion/organizations/3/" \
  -H "Authorization: Token your-api-token"
```

**Response:** `204 No Content`

⚠️ **Note:** Deleting an organization will automatically delete all associated ISD-ASes due to CASCADE relationship.

---

## 🏗️ ISD-AS API

Manage SCION ISD-AS (Isolation Domain - Autonomous System) identifiers.

### Base Endpoint
```
/api/plugins/scion/isd-ases/
```

### List ISD-ASes

**GET** `/api/plugins/scion/isd-ases/`

```bash
curl -X GET \
  "https://netbox.example.com/api/plugins/scion/isd-ases/" \
  -H "Authorization: Token your-api-token" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "count": 2,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "url": "https://netbox.example.com/api/plugins/scion/isd-ases/1/",
      "display": "1-ff00:0:110",
      "isd_as": "1-ff00:0:110",
      "description": "Core ISD-AS for ACME network",
      "organization": {
        "id": 1,
        "url": "https://netbox.example.com/api/plugins/scion/organizations/1/",
        "display": "ACME"
      },
      "appliances": ["border1.acme.com", "border2.acme.com"],
      "appliances_display": "border1.acme.com, border2.acme.com",
      "created": "2025-09-09T10:30:00.000000Z",
      "last_updated": "2025-09-09T10:30:00.000000Z",
      "custom_field_data": {}
    },
    {
      "id": 2,
      "url": "https://netbox.example.com/api/plugins/scion/isd-ases/2/",
      "display": "12-332",
      "isd_as": "12-332",
      "description": "",
      "organization": {
        "id": 2,
        "url": "https://netbox.example.com/api/plugins/scion/organizations/2/",
        "display": "EXAMPLE"
      },
      "appliances": ["router1.example.com"],
      "appliances_display": "router1.example.com",
      "created": "2025-09-09T11:00:00.000000Z",
      "last_updated": "2025-09-09T11:00:00.000000Z",
      "custom_field_data": {}
    }
  ]
}
```

### Get ISD-AS

**GET** `/api/plugins/scion/isd-ases/{id}/`

```bash
curl -X GET \
  "https://netbox.example.com/api/plugins/scion/isd-ases/1/" \
  -H "Authorization: Token your-api-token" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "id": 1,
  "url": "https://netbox.example.com/api/plugins/scion/isd-ases/1/",
  "display": "1-ff00:0:110", 
  "isd_as": "1-ff00:0:110",
  "description": "Core ISD-AS for ACME network providing transit services",
  "organization": {
    "id": 1,
    "url": "https://netbox.example.com/api/plugins/scion/organizations/1/",
    "display": "ACME"
  },
  "appliances": ["border1.acme.com", "border2.acme.com", "transit1.acme.com"],
  "appliances_display": "border1.acme.com, border2.acme.com, transit1.acme.com",
  "created": "2025-09-09T10:30:00.000000Z",
  "last_updated": "2025-09-09T10:30:00.000000Z",
  "custom_field_data": {}
}
```

### Create ISD-AS

**POST** `/api/plugins/scion/isd-ases/`

```bash
curl -X POST \
  "https://netbox.example.com/api/plugins/scion/isd-ases/" \
  -H "Authorization: Token your-api-token" \
  -H "Content-Type: application/json" \
  -d '{
    "isd_as": "2-ff00:0:220",
    "organization": 1,
    "appliances": ["core1.newnet.com", "core2.newnet.com"],
    "description": "New ISD-AS for expanded network"
  }'
```

**Request Body:**
```json
{
  "isd_as": "2-ff00:0:220",
  "organization": 1,
  "appliances": ["core1.newnet.com", "core2.newnet.com"],
  "description": "New ISD-AS for expanded network"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "url": "https://netbox.example.com/api/plugins/scion/isd-ases/3/",
  "display": "2-ff00:0:220",
  "isd_as": "2-ff00:0:220", 
  "description": "New ISD-AS for expanded network",
  "organization": {
    "id": 1,
    "url": "https://netbox.example.com/api/plugins/scion/organizations/1/",
    "display": "ACME"
  },
  "appliances": ["core1.newnet.com", "core2.newnet.com"],
  "appliances_display": "core1.newnet.com, core2.newnet.com",
  "created": "2025-09-09T12:30:00.000000Z",
  "last_updated": "2025-09-09T12:30:00.000000Z",
  "custom_field_data": {}
}
```

### Update ISD-AS

**PATCH** `/api/plugins/scion/isd-ases/{id}/`

```bash
curl -X PATCH \
  "https://netbox.example.com/api/plugins/scion/isd-ases/3/" \
  -H "Authorization: Token your-api-token" \
  -H "Content-Type: application/json" \
  -d '{
    "appliances": ["core1.newnet.com", "core2.newnet.com", "backup1.newnet.com"]
  }'
```

### Delete ISD-AS

**DELETE** `/api/plugins/scion/isd-ases/{id}/`

```bash
curl -X DELETE \
  "https://netbox.example.com/api/plugins/scion/isd-ases/3/" \
  -H "Authorization: Token your-api-token"
```

**Response:** `204 No Content`

---

## 🔗 SCION Link Assignments API

Manage SCION link interface assignments with customer information.

### Base Endpoint
```
/api/plugins/scion/link-assignments/
```

### List Link Assignments

**GET** `/api/plugins/scion/link-assignments/`

```bash
curl -X GET \
  "https://netbox.example.com/api/plugins/scion/link-assignments/" \
  -H "Authorization: Token your-api-token" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "count": 3,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "url": "https://netbox.example.com/api/plugins/scion/link-assignments/1/",
      "display": "1-ff00:0:110 - Interface 1",
      "isd_as": {
        "id": 1,
        "url": "https://netbox.example.com/api/plugins/scion/isd-ases/1/",
        "display": "1-ff00:0:110"
      },
      "core": "border1.acme.com",
      "interface_id": 1,
      "relationship": "CHILD",
      "customer_id": "CUST001",
      "peer_name": "Customer Networks Ltd",
      "peer": "12-332#2",
      "zendesk_ticket": "12345",
      "created": "2025-09-09T11:30:00.000000Z",
      "last_updated": "2025-09-09T11:30:00.000000Z",
      "custom_field_data": {}
    },
    {
      "id": 2,
      "url": "https://netbox.example.com/api/plugins/scion/link-assignments/2/",
      "display": "1-ff00:0:110 - Interface 2",
      "isd_as": {
        "id": 1,
        "url": "https://netbox.example.com/api/plugins/scion/isd-ases/1/",
        "display": "1-ff00:0:110"
      },
      "core": "border2.acme.com",
      "interface_id": 2,
      "relationship": "PARENT",
      "customer_id": "UPSTREAM001",
      "peer_name": "Upstream Provider Inc",
      "peer": "1-ff00:0:100#5",
      "zendesk_ticket": "",
      "created": "2025-09-09T11:45:00.000000Z",
      "last_updated": "2025-09-09T11:45:00.000000Z",
      "custom_field_data": {}
    }
  ]
}
```

### Get Link Assignment

**GET** `/api/plugins/scion/link-assignments/{id}/`

```bash
curl -X GET \
  "https://netbox.example.com/api/plugins/scion/link-assignments/1/" \
  -H "Authorization: Token your-api-token" \
  -H "Content-Type: application/json"
```

**Response:**
```json
{
  "id": 1,
  "url": "https://netbox.example.com/api/plugins/scion/link-assignments/1/",
  "display": "1-ff00:0:110 - Interface 1",
  "isd_as": {
    "id": 1,
    "url": "https://netbox.example.com/api/plugins/scion/isd-ases/1/",
    "display": "1-ff00:0:110"
  },
  "core": "border1.acme.com",
  "interface_id": 1,
  "relationship": "CHILD",
  "customer_id": "CUST001",
  "peer_name": "Customer Networks Ltd",
  "peer": "12-332#2",
  "zendesk_ticket": "12345",
  "created": "2025-09-09T11:30:00.000000Z",
  "last_updated": "2025-09-09T11:30:00.000000Z",
  "custom_field_data": {}
}
```

### Create Link Assignment

**POST** `/api/plugins/scion/link-assignments/`

```bash
curl -X POST \
  "https://netbox.example.com/api/plugins/scion/link-assignments/" \
  -H "Authorization: Token your-api-token" \
  -H "Content-Type: application/json" \
  -d '{
    "isd_as": 1,
    "core": "border1.acme.com",
    "interface_id": 3,
    "relationship": "CORE",
    "customer_id": "CORE001",
    "peer_name": "Core Partner",
    "peer": "3-ff00:0:300#1",
    "zendesk_ticket": "54321"
  }'
```

**Request Body:**
```json
{
  "isd_as": 1,
  "core": "border1.acme.com", 
  "interface_id": 3,
  "relationship": "CORE",
  "customer_id": "CORE001",
  "peer_name": "Core Partner",
  "peer": "3-ff00:0:300#1",
  "zendesk_ticket": "54321"
}
```

**Response (201 Created):**
```json
{
  "id": 3,
  "url": "https://netbox.example.com/api/plugins/scion/link-assignments/3/",
  "display": "1-ff00:0:110 - Interface 3",
  "isd_as": {
    "id": 1,
    "url": "https://netbox.example.com/api/plugins/scion/isd-ases/1/",
    "display": "1-ff00:0:110"
  },
  "core": "border1.acme.com",
  "interface_id": 3,
  "relationship": "CORE",
  "customer_id": "CORE001", 
  "peer_name": "Core Partner",
  "peer": "3-ff00:0:300#1",
  "zendesk_ticket": "54321",
  "created": "2025-09-09T13:00:00.000000Z",
  "last_updated": "2025-09-09T13:00:00.000000Z",
  "custom_field_data": {}
}
```

### Update Link Assignment

**PATCH** `/api/plugins/scion/link-assignments/{id}/`

```bash
curl -X PATCH \
  "https://netbox.example.com/api/plugins/scion/link-assignments/3/" \
  -H "Authorization: Token your-api-token" \
  -H "Content-Type: application/json" \
  -d '{
    "peer_name": "Updated Core Partner Name",
    "zendesk_ticket": "55555"
  }'
```

### Delete Link Assignment

**DELETE** `/api/plugins/scion/link-assignments/{id}/`

```bash
curl -X DELETE \
  "https://netbox.example.com/api/plugins/scion/link-assignments/3/" \
  -H "Authorization: Token your-api-token"
```

**Response:** `204 No Content`

---

## 🔍 Filtering and Search

All list endpoints support filtering and search parameters.

### Common Filter Parameters

#### Organizations
- `short_name`: Filter by organization short name
- `q`: Search in short_name, full_name, and description

```bash
# Search for organizations containing "acme"
curl "https://netbox.example.com/api/plugins/scion/organizations/?q=acme"

# Filter by exact short name
curl "https://netbox.example.com/api/plugins/scion/organizations/?short_name=ACME"
```

#### ISD-ASes
- `isd_as`: Filter by ISD-AS identifier
- `organization`: Filter by organization ID
- `organization__short_name`: Filter by organization short name
- `q`: Search in isd_as, description, and organization fields

```bash
# Filter by organization
curl "https://netbox.example.com/api/plugins/scion/isd-ases/?organization=1"

# Filter by organization short name
curl "https://netbox.example.com/api/plugins/scion/isd-ases/?organization__short_name=ACME"

# Search across multiple fields
curl "https://netbox.example.com/api/plugins/scion/isd-ases/?q=ff00"
```

#### Link Assignments
- `isd_as`: Filter by ISD-AS ID
- `isd_as__isd_as`: Filter by ISD-AS identifier
- `relationship`: Filter by relationship type (PARENT, CHILD, CORE)
- `customer_id`: Filter by customer ID
- `peer_name`: Filter by peer name
- `peer`: Filter by peer identifier
- `q`: Search across customer_id, peer_name, and zendesk_ticket

```bash
# Filter by relationship type
curl "https://netbox.example.com/api/plugins/scion/link-assignments/?relationship=CHILD"

# Filter by ISD-AS identifier
curl "https://netbox.example.com/api/plugins/scion/link-assignments/?isd_as__isd_as=1-ff00:0:110"

# Search for customer information
curl "https://netbox.example.com/api/plugins/scion/link-assignments/?q=customer"
```

### Pagination

All list endpoints support pagination:

```bash
# Get first 20 results
curl "https://netbox.example.com/api/plugins/scion/organizations/?limit=20"

# Get next page
curl "https://netbox.example.com/api/plugins/scion/organizations/?limit=20&offset=20"
```

---

## 📤 Export Formats

List endpoints support CSV export by adding `?format=csv`:

```bash
# Export organizations to CSV
curl "https://netbox.example.com/api/plugins/scion/organizations/?format=csv" \
  -H "Authorization: Token your-api-token"

# Export ISD-ASes to CSV  
curl "https://netbox.example.com/api/plugins/scion/isd-ases/?format=csv" \
  -H "Authorization: Token your-api-token"

# Export link assignments to CSV
curl "https://netbox.example.com/api/plugins/scion/link-assignments/?format=csv" \
  -H "Authorization: Token your-api-token"
```

---

## ⚠️ Error Handling

### Common HTTP Status Codes

- `200 OK`: Successful GET request
- `201 Created`: Successful POST request (resource created)
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Invalid or missing authentication
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

### Error Response Format

```json
{
  "error": "Validation failed",
  "details": {
    "isd_as": ["ISD-AS must be in format '{isd}-{as}' (e.g., '1-ff00:0:110' or '1-1')"],
    "organization": ["This field is required."]
  }
}
```

### Validation Rules

#### Organization
- `short_name`: Required, unique, max 100 characters
- `full_name`: Required, max 200 characters

#### ISD-AS
- `isd_as`: Required, unique, must match format `{isd}-{as}` (e.g., `1-ff00:0:110` or `1-1`)
- `organization`: Required, must reference existing organization
- `appliances`: Optional JSON array

#### Link Assignment
- `isd_as`: Required, must reference existing ISD-AS
- `interface_id`: Required, positive integer, unique per ISD-AS
- `relationship`: Required, must be one of: PARENT, CHILD, CORE
- `customer_id`: Required, max 100 characters
- `peer_name`: Required, max 100 characters  
- `peer`: Required, max 255 characters, unique per ISD-AS
- `zendesk_ticket`: Optional, numbers only, max 16 characters

---

## 🔧 Python Examples

### Using Python Requests

```python
import requests
import json

# Configuration
BASE_URL = "https://netbox.example.com/api/plugins/scion"
TOKEN = "your-api-token"
HEADERS = {
    "Authorization": f"Token {TOKEN}",
    "Content-Type": "application/json"
}

# Create an organization
org_data = {
    "short_name": "PYTHONORG",
    "full_name": "Python Test Organization",
    "description": "Created via API"
}

response = requests.post(
    f"{BASE_URL}/organizations/",
    headers=HEADERS,
    data=json.dumps(org_data)
)

if response.status_code == 201:
    org = response.json()
    print(f"Created organization: {org['display']}")
    
    # Create an ISD-AS for this organization
    isdas_data = {
        "isd_as": "99-test:0:1",
        "organization": org["id"],
        "appliances": ["test1.example.com"],
        "description": "Test ISD-AS created via API"
    }
    
    isdas_response = requests.post(
        f"{BASE_URL}/isd-ases/",
        headers=HEADERS,
        data=json.dumps(isdas_data)
    )
    
    if isdas_response.status_code == 201:
        isdas = isdas_response.json()
        print(f"Created ISD-AS: {isdas['display']}")
        
        # Create a link assignment
        link_data = {
            "isd_as": isdas["id"],
            "core": "test1.example.com",
            "interface_id": 1,
            "relationship": "CHILD",
            "customer_id": "TEST001",
            "peer_name": "Test Peer",
            "peer": "99-test:0:2#1",
            "zendesk_ticket": "99999"
        }
        
        link_response = requests.post(
            f"{BASE_URL}/link-assignments/",
            headers=HEADERS,
            data=json.dumps(link_data)
        )
        
        if link_response.status_code == 201:
            link = link_response.json()
            print(f"Created link assignment: {link['display']}")

# List all organizations
response = requests.get(f"{BASE_URL}/organizations/", headers=HEADERS)
if response.status_code == 200:
    data = response.json()
    print(f"Total organizations: {data['count']}")
    for org in data['results']:
        print(f"- {org['short_name']}: {org['full_name']}")
```

---

## 📝 Notes

1. **Unique Constraints:**
   - Organization `short_name` must be unique globally
   - ISD-AS `isd_as` identifier must be unique globally
   - Link Assignment `interface_id` must be unique per ISD-AS
   - Link Assignment `peer` identifier must be unique per ISD-AS

2. **Cascading Deletes:**
   - Deleting an organization will delete all associated ISD-ASes
   - Deleting an ISD-AS will delete all associated link assignments

3. **Peer Field Format:**
   - The `peer` field should follow the format `{isd}-{as}#{interface_number}`
   - Examples: `1-ff00:0:110#1`, `12-332#2`, `3-ff00:0:300#1`

4. **Zendesk Integration:**
   - Zendesk ticket field accepts numbers only
   - Links to `https://anapaya.zendesk.com/agent/tickets/{ticket_number}`

For more information, refer to the main plugin documentation or NetBox API documentation.
