***# Contract A — Backend API Proposal (Draft)***



***Author: Person 2 (backend). Status: DRAFT — not yet agreed with Person 1/Person 3.***

***Base: FastAPI. All responses JSON. All endpoints prefixed `/api/v1`.***



***## 1. Health check***

***`GET /api/v1/health`***

***→ `{"status": "ok"}`***



***## 2. Search***

***`GET /api/v1/objects/search?q=<text>\&category=<id>\&limit=<n>`***

***- `q`: matches against object `name`***

***- `category`: optional, filters by category\_id (1-7)***

***- `limit`: default 20, max 100***

***→***

***```json***

***{***

&#x20; ***"results": \[***

&#x20;   ***{"object\_id": 1, "name": "ISS (ZARYA)", "norad\_id": 25544, "category\_id": 1}***

&#x20; ***],***

&#x20; ***"count": 1***

***}***

***```***



***## 3. Category filter / listing***

***`GET /api/v1/objects?category=<id>\&limit=<n>\&offset=<n>`***

***→ same shape as search results, paginated.***



***## 4. Object lookup / details***

***`GET /api/v1/objects/{object\_id}`***

***→***

***```json***

***{***

&#x20; ***"object\_id": 1,***

&#x20; ***"name": "ISS (ZARYA)",***

&#x20; ***"norad\_id": 25544,***

&#x20; ***"cospar\_id": "1998-067A",***

&#x20; ***"category\_id": 1,***

&#x20; ***"resolved\_metadata": {***

&#x20;   ***"operator": "NASA/Roscosmos",***

&#x20;   ***"launch\_date": "1998-11-20",***

&#x20;   ***"manufacturer": "..."***

&#x20; ***}***

***}***

***```***

***(`resolved\_metadata` pulled from the `resolved\_metadata` table — one clean value per field.)***



***## 5. Orbital state (Contract C)***

***`GET /api/v1/objects/{object\_id}/state`***

***→ exact output of `state\_model.get\_state()` — already built:***

***```json***

***{***

&#x20; ***"object\_id": 1,***

&#x20; ***"position": \[x, y, z],***

&#x20; ***"velocity": \[vx, vy, vz],***

&#x20; ***"altitude": 417.9,***

&#x20; ***"epoch": "2026-08-13T03:34:14",***

&#x20; ***"frame": "TEME",***

&#x20; ***"source": "Space-Track",***

&#x20; ***"age\_hours": 8.24,***

&#x20; ***"status": "fresh"***

***}***

***```***



***## 6. Media***

***`GET /api/v1/objects/{object\_id}/media`***

***→***

***```json***

***{"object\_id": 1, "media": \[{"url": "...", "media\_type": "image", "source": "SatNOGS"}]}***

***```***



***## 7. Diagnostics (dev-only, for Person 3)***

***`GET /api/v1/objects/{object\_id}/diagnostics`***

***→ exact output of `diagnostics.get\_diagnostics()` — already built (raw orbital\_elements row, SGP4 error code, staleness detail, ingestion history).***



***---***



***## Open questions for Person 1 / Person 3***

***- Pagination style OK (`limit`/`offset`), or prefer cursor-based?***

***- Error shape for not-found objects — proposal: `404` + `{"error": "object not found"}`.***

***- Auth needed on any endpoint, or all public reads for now?***

***- Rate limiting needed at API layer, or handled elsewhere?***

