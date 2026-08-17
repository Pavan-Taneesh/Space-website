# Contract A — Backend API Proposal (Draft)

Author: Person 2 (backend). Status: DRAFT — not yet agreed with Person 1/Person 3.
Base: FastAPI. All responses JSON. All endpoints prefixed `/api/v1`.

## 1. Health check
`GET /api/v1/health`
→ `{"status": "ok"}`

## 2. Search
`GET /api/v1/objects/search?q=<text>&category=<id>&limit=<n>`
- `q`: matches against object `name`
- `category`: optional, filters by category_id (1-7)
- `limit`: default 20, max 100
→
```json
{
  "results": [
    {"object_id": 1, "name": "ISS (ZARYA)", "norad_id": 25544, "category_id": 1}
  ],
  "count": 1
}
```

## 3. Category filter / listing
`GET /api/v1/objects?category=<id>&limit=<n>&offset=<n>`
→ same shape as search results, paginated.

## 4. Object lookup / details
`GET /api/v1/objects/{object_id}`
→
```json
{
  "object_id": 1,
  "name": "ISS (ZARYA)",
  "norad_id": 25544,
  "cospar_id": "1998-067A",
  "category_id": 1,
  "resolved_metadata": {
    "operator": "NASA/Roscosmos",
    "launch_date": "1998-11-20",
    "manufacturer": "..."
  }
}
```
(`resolved_metadata` pulled from the `resolved_metadata` table — one clean value per field.)

## 5. Orbital state (Contract C)
`GET /api/v1/objects/{object_id}/state`
→ exact output of `state_model.get_state()` — already built:
```json
{
  "object_id": 1,
  "position": [x, y, z],
  "velocity": [vx, vy, vz],
  "altitude": 417.9,
  "epoch": "2026-08-13T03:34:14",
  "frame": "TEME",
  "source": "Space-Track",
  "age_hours": 8.24,
  "status": "fresh"
}
```

## 6. Media
`GET /api/v1/objects/{object_id}/media`
→
```json
{"object_id": 1, "media": [{"url": "...", "media_type": "image", "source": "SatNOGS"}]}
```

## 7. Diagnostics (dev-only, for Person 3)
`GET /api/v1/objects/{object_id}/diagnostics`
→ exact output of `diagnostics.get_diagnostics()` — already built (raw orbital_elements row, SGP4 error code, staleness detail, ingestion history).

---

## Open questions for Person 1 / Person 3
- Pagination style OK (`limit`/`offset`), or prefer cursor-based?
- Error shape for not-found objects — proposal: `404` + `{"error": "object not found"}`.
- Auth needed on any endpoint, or all public reads for now?
- Rate limiting needed at API layer, or handled elsewhere?