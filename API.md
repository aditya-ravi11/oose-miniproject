# API Guide

Base URL (dev): `http://localhost:8000`

## Auth
### POST /auth/register
Request:
```json
{
  "name": "Citizen",
  "email": "citizen@example.com",
  "phone": "+91-9000000000",
  "password": "Passw0rd!"
}
```
Response `200`:
```json
{
  "access_token": "jwt",
  "token_type": "bearer",
  "user": {"id": "...", "name": "Citizen", "email": "citizen@example.com", "role": "citizen"}
}
```

### POST /auth/login
Body `{ "email": "...", "password": "..." }` ? same token response.

### GET /auth/me
Bearer-protected. Returns the authenticated user profile.

## Requests
### POST /requests
Creates a pickup request (state starts at `submitted`).
```json
{
  "category": "recyclable",
  "is_special": false,
  "description": "Old newspapers & plastic bottles",
  "quantity": 3,
  "address": {
    "line1": "B-102, Somaiya Hostel",
    "city": "Mumbai",
    "pincode": "400077",
    "lat": 19.072,
    "lng": 72.899
  },
  "preferred_slots": [
    {"start": "2025-08-10T09:00:00+00:00", "end": "2025-08-10T10:00:00+00:00"}
  ],
  "photos": ["/uploads/2025/08/uuid1.jpg"]
}
```

### GET /requests
Query params: `status`, `category`, `skip`, `limit`. Returns `{ items: [...], total, skip, limit }`.

### GET /requests/{id}
Returns the caller's request with full timeline.

### POST /requests/{id}/cancel
Body `{ "reason": "..." }` (optional). Allowed statuses: `draft|submitted|scheduled` and must be >24h before confirmed slot start.

### POST /requests/{id}/confirm-slot
Body `{ "slot_start": "ISO", "slot_end": "ISO" }` to accept a proposed schedule.

## Slots
### GET /slots/available
Query parameters:
- `date`: `YYYY-MM-DD`
- `category`: request category
Returns a list of `{ start, end }` windows respecting capacity + conflicts.

## Files
### POST /files/upload
Multipart field `file`. Stores under `/uploads/<yyyy>/<mm>/uuid.ext` and returns:
```json
{ "url": "http://localhost:8000/uploads/2024/07/abc.jpg", "path": "2024/07/abc.jpg" }
```

## Notifications
### GET /notifications
Returns latest notifications for the authenticated user.

### WebSocket /ws/notifications
Connect with `ws://host/ws/notifications?token=<JWT>`. Messages mirror notification documents `{ id, title, body, channel, meta }`.

## Rewards
### GET /rewards/summary
Returns:
```json
{
  "total_points": 25,
  "recent": [
    {"id": "...", "points": 5, "reason": "Completed recyclable pickup", "created_at": "..."}
  ]
}
```

## Status Flow
```
draft -> submitted -> pending_review -> scheduled -> enroute -> onsite -> collecting -> collected -> handover -> verification -> completed
any      -> cancelled
(enroute|onsite) -> failed -> scheduled (manual) or cancelled
```

## Notifications Rules
- Email + in-app on submit.
- Email when slot confirmed.
- Queue entries stored with `status=queued`, drained by APScheduler.
- SMS / Push available once feature flags are enabled (`ENABLE_SMS`, `ENABLE_PUSH`).

## Reward Rules
- +5 points when a recyclable request reaches `completed`.
- +10 points when an e-waste or hazardous request completes.
- Rewards stored in `rewards` and surfaced through `/rewards/summary` and the UI badge.