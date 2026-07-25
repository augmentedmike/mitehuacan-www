# MiTehuacán (combi-tracker)

Open-source crowd-mapping of Mexico's informal transit (combis/colectivos): find and
plan combi trips, while consenting riders' phones passively keep the map alive.
First city: **Tehuacán, Puebla**. Production site: **https://mitehuacan.mx** (directory
per city: `/tehuacan`; QR stickers resolve via `/qr/<sticker-id>` and never break).

**Code:** AGPL-3.0 (`LICENSE`) · **Data:** ODbL 1.0 (`data-LICENSE.md`) · **Security & privacy:** [`SECURITY.md`](SECURITY.md)

## What's here

| Path | What |
|---|---|---|
| `apps/www/` | The web app: frontend (`app/`), API (`functions/`), build/data scripts (`scripts/`), DB migrations (`migrations/`) |
| `apps/admin/` | Coordinator web app (Traccar-based ride collection pipeline) |
| `apps/ios/` | Native iOS app: planner + passive telemetry + crowding tags |
| `apps/backup/` | D1 backup Worker — nightly archive + restore tooling |
| `planning/` | Docs (`docs/`), PRDs (`prds/`), business plans (`business/`), financial models (`financials/`) |
| `build/` | Generated mitehuacan.mx static site |
| `resources/` | Data artifacts (brand, map-data, POIs, stickers) |
| `infra/` | Infrastructure (Traccar) |
| `SECURITY.md` | Rules for humans and AI agents; location data is radioactive |

## Status / decisions (2026-07)

- Launch architecture: **Tier 0** (Cloudflare Pages + Worker + D1, nightly processing) — see system design §6
- Mobile v0: **planner + manual ride recording**; passive auto-collection in v1
- Distribution: QR stickers on combis/stops → landing page → web map + store links
- Next build targets: Tier 0 ingest worker + D1 schema · landing page · Expo v0 scaffold

## Quick start (web map)

```bash
cd tehuacan/map && python3 -m http.server 8123
# open http://localhost:8123 — needs internet for basemap tiles + geocoding
```

Dataset rebuild: `apps/www/scripts/01…08` in order (see `tehuacan/README.md`).
