# MiTehuacán (combi-tracker)

Open-source crowd-mapping of Mexico's informal transit (combis/colectivos). Find and
plan combi trips; consenting riders' phones passively keep the map alive.
First city: **Tehuacán, Puebla**. Site: **https://mitehuacan.mx**

**Code:** AGPL-3.0 (`LICENSE`) · **Data:** ODbL 1.0 (`data-LICENSE.md`)

## Quick start

```bash
python3 apps/www/scripts/09_build_site.py   # rebuild the site
./dev.sh                                     # local dev server on :8799
```

After building, open `build/combis/` in a browser. Needs internet for basemap tiles + geocoding.

## What's here

| Path | What |
|---|---|
| `apps/www/` | Web app: frontend (`app/`), API (`functions/`), build/scrape scripts (`scripts/`), DB migrations |
| `apps/admin/` | Coordinator web app (Traccar ride collection pipeline) |
| `apps/ios/` | Native iOS app — planner + passive telemetry + crowding tags |
| `apps/backup/` | D1 backup Worker — nightly archive + restore tooling |
| `planning/` | Docs, PRDs, business plans, financials (private submodule) |
| `build/` | Generated static site (never edit by hand) |
| `resources/` | Data artifacts: brand, map-data, POIs, stickers, raw scrapes |
| `infra/` | Traccar Docker Compose for route recording sessions |

## More detail

See [`planning/docs/project-map.md`](planning/docs/project-map.md) for the full architecture:
repos, apps, folder rationale, data flow, deploy commands, and a quick reference.
