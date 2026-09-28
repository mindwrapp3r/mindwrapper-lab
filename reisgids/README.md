# reisgids

An agent skill (Claude Code / any agent that reads `SKILL.md`) that plans trips into an Obsidian vault: a travel profile it reads first, one note per place with verified coordinates, a route document, a trip note that ties them together, and a single Markdown export for voice mode on the road. The skill itself is written in Dutch.

Een agent-skill die reizen plant in een Obsidian-vault: eerst een reisprofiel lezen, één notitie per plek met gecontroleerde coördinaten, een routedocument, een Trip-notitie die alles koppelt, en één Markdown-export voor voice mode onderweg.

## Contents

- `SKILL.md`: the workflow, step by step
- `scripts/geocode.py`: look up and check coordinates against OpenStreetMap (Nominatim + Overpass)
- `scripts/export_onderweg.py`: build the on-the-road export: `uv run scripts/export_onderweg.py --vault ~/path/to/vault "<Trip note>"`
- `references/reislog-formaat.md`: the daily travel-log format that voice mode returns and the skill reads back

## What you need

- [uv](https://docs.astral.sh/uv/) (scripts use PEP 723 inline dependencies)
- An Obsidian vault with a `Places` folder, a `Trips` category and a travel profile note. The folder names in `SKILL.md` are an example layout; change them to match yours
- Write your own `Reisprofiel.md`: who travels, what makes a trip good, what disappoints. That profile is what makes the advice personal

## Known limitation

Voice mode in the ChatGPT and Claude apps can't safely talk to the vault directly, so the export is a copy: re-export when the plan changes.
