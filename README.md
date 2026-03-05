# NumGen PLB 2021

VDP nummer generator voor etiketten productie. Genereert genummerde CSV/Excel bestanden voor Variable Data Printing (VDP) met rol-structuur, SSCC check digits, en multi-taal sluitetiketten.

## Status

**Migrated to Django** — The core logic has been ported to the Django web app at:
`/Users/miketenhoonte/PRODUCTION/DJANGO-l02-app03-dev/numgen/`

This repository contains the original standalone PyQt5 version (previously PySimpleGUI).

## What it does

1. Generates sequential number lists with optional SSCC-18 check digits
2. Supports prefix/postfix, template formatting (`?` placeholders for human-readable output)
3. Splits numbers into rolls with inloop/uitloop, wikkel, and sluitetiketten
4. Distributes across multiple VDPs with mes (knife) alignment
5. Exports CSV and Excel files ready for VDP production

## Key modules

| Module | Purpose |
|--------|---------|
| `calculations/calculations.py` | DataFrame ops, roll splitting, wikkel formula |
| `calculations/character_template.py` | Template system (`?` → digit replacement) |
| `calculations/sscc_cd_calc.py` | GS1 SSCC check digit calculation |
| `data/data_definitions.py` | Number list builders, roll structure, summaries |

## Django version

The Django port lives at `/Users/miketenhoonte/PRODUCTION/DJANGO-l02-app03-dev/numgen/` and includes:
- Web form with 28 fields (order, numbers, rolls, slicing, templates, SSCC, language)
- Job tracking with history and artifact downloads
- 95 automated tests (`uv run pytest numgen/ -v`)
- Full documentation in `HANDOFF.md`
