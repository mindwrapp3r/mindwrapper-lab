#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["httpx", "pyyaml"]
# ///
"""Coördinaten opzoeken en controleren via OpenStreetMap (Nominatim).

Twee modi:

  zoek   "<plek, stad>" [--limit 3]
         Geeft kandidaten met lat/lon, adres en een Google Maps-link.

  rond   "<naam-regex>" --bij LAT,LON [--straal 500]
         Zoekt via Overpass objecten met een naam die matcht in een straal. Voor zaken
         die in OSM anders heten (Casa Montaña = "Bodega Montaña") en voor
         parkeergarages: die geven de inrit (amenity=parking_entrance) als apart object.

  check  <notitie.md> [<notitie.md> ...] [--max-afstand 75]
         Leest `coordinates` en `address` uit de frontmatter van Places-notities,
         zoekt de plek op en meldt de afwijking in meters. Alles boven
         --max-afstand krijgt het label AFWIJKING.

Nominatim staat 1 verzoek per seconde toe; het script wacht zelf.
Een lege uitslag betekent "OSM kent deze naam niet", niet "de plek bestaat niet":
probeer dan het adres, een andere spelling of de officiële naam.
"""

import argparse
import json
import math
import re
import sys
import time
import urllib.parse
from pathlib import Path

import httpx
import yaml

UA = "reisgids-skill/1.0 (+https://github.com/mindwrapp3r/mindwrapper-lab)"
URL = "https://nominatim.openstreetmap.org/search"
_last = 0.0


def nominatim(q: str, limit: int = 3, rond: tuple[float, float] | None = None) -> list[dict]:
    global _last
    wait = 1.1 - (time.monotonic() - _last)
    if wait > 0:
        time.sleep(wait)
    r = httpx.get(
        URL,
        params={"q": q, "format": "jsonv2", "limit": limit, "addressdetails": 0}
        | ({"viewbox": f"{rond[1]-0.04},{rond[0]+0.03},{rond[1]+0.04},{rond[0]-0.03}", "bounded": 1} if rond else {}),
        headers={"User-Agent": UA, "Accept-Language": "nl,en"},
        timeout=20,
    )
    _last = time.monotonic()
    r.raise_for_status()
    return r.json()


def maps_link(query: str) -> str:
    return "https://www.google.com/maps/search/?api=1&query=" + urllib.parse.quote_plus(query)


def meters(a: tuple[float, float], b: tuple[float, float]) -> float:
    la1, lo1, la2, lo2 = map(math.radians, (*a, *b))
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * 6371000 * math.asin(math.sqrt(h))


def frontmatter(p: Path) -> dict:
    t = p.read_text(encoding="utf-8")
    if not t.startswith("---"):
        return {}
    return yaml.safe_load(t.split("---", 2)[1]) or {}


def stad_uit(adres: str) -> str | None:
    """'C. Alcazabilla, 2, 29012 Málaga, Spanje' -> 'Málaga' (het deel met de postcode)."""
    for deel in adres.split(","):
        if m := re.match(r"\s*\d{4,5}\s+(.+)", deel):
            return m.group(1).strip()
    return None


def cmd_zoek(args) -> int:
    res = nominatim(args.query, args.limit)
    out = [
        {
            "lat": f"{float(r['lat']):.7f}",
            "lon": f"{float(r['lon']):.7f}",
            "naam": r.get("name"),
            "adres": r.get("display_name"),
            "type": f"{r.get('category')}/{r.get('type')}",
            "maps": maps_link(r.get("display_name") or args.query),
        }
        for r in res
    ]
    print(json.dumps(out, ensure_ascii=False, indent=2))
    return 0 if out else 1


def cmd_check(args) -> int:
    fouten = 0
    for f in args.notities:
        p = Path(f)
        fm = frontmatter(p)
        naam = p.stem
        coords = fm.get("coordinates") or []
        if len(coords) != 2:
            print(f"GEEN COÖRDINATEN  {naam}")
            fouten += 1
            continue
        eigen = (float(coords[0]), float(coords[1]))
        # Volgorde: naam + adres, dan naam en aliases + stad, en pas als laatste het kale adres.
        # Het kale adres geeft bij "s/n" of een lange straat het midden van de straat terug,
        # en dan wordt een correct punt ten onrechte AFWIJKING
        pogingen = [f"{naam}, {fm['address']}" if fm.get("address") else naam]
        stad = args.stad or stad_uit(str(fm.get("address") or ""))
        for n in [naam, *(fm.get("aliases") or [])]:
            pogingen.append(f"{n}, {stad}" if stad else str(n))
        if fm.get("address"):
            pogingen.append(str(fm["address"]))
        hit, raak = None, None
        for q in dict.fromkeys(pogingen):
            # Alleen zoeken rond het eigen punt (~3 km): "<naam>, <stad>" vindt anders
            # een naamgenoot aan de andere kant van het land
            res = nominatim(q, 1, rond=eigen)
            if res:
                hit, raak = res[0], q
                break
        if not hit:
            print(f"NIET GEVONDEN     {naam}  (controleer handmatig)")
            continue
        osm = (float(hit["lat"]), float(hit["lon"]))
        d = meters(eigen, osm)
        soort = f"{hit.get('category')}/{hit.get('type')}"
        grof = hit.get("category") in ("highway", "place", "boundary")
        label = "AFWIJKING" if d > args.max_afstand else "ok"
        if d > args.max_afstand:
            fouten += 1
        print(f"{label:<17} {naam}  {d:>5.0f} m  osm={osm[0]:.7f},{osm[1]:.7f}  [{soort}]")
        print(f"{'':<17}   gezocht: {raak!r}" + ("  ← straat/plein: grof referentiepunt, beoordeel zelf" if grof else ""))
    return 1 if fouten else 0


def cmd_rond(args) -> int:
    lat, lon = (float(x) for x in args.bij.split(","))
    q = f'''[out:json][timeout:25];
nwr(around:{args.straal},{lat},{lon})["name"~"{args.regex}",i];
out center 20;'''
    r = httpx.post("https://overpass-api.de/api/interpreter", data={"data": q}, headers={"User-Agent": UA}, timeout=40)
    r.raise_for_status()
    out = []
    for e in r.json().get("elements", []):
        c = e.get("center") or e
        t = e.get("tags", {})
        soort = next((f"{k}={t[k]}" for k in ("amenity", "shop", "tourism", "leisure", "historic") if k in t), "")
        d = meters((lat, lon), (c["lat"], c["lon"]))
        out.append((d, f"{c['lat']:.7f},{c['lon']:.7f}  {t.get('name')}  [{soort}]  {d:.0f} m"))
    for _, regel in sorted(out):
        print(regel)
    return 0 if out else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    z = sub.add_parser("zoek")
    z.add_argument("query")
    z.add_argument("--limit", type=int, default=3)
    r = sub.add_parser("rond")
    r.add_argument("regex")
    r.add_argument("--bij", required=True, help="LAT,LON")
    r.add_argument("--straal", type=int, default=500)
    c = sub.add_parser("check")
    c.add_argument("notities", nargs="+")
    c.add_argument("--max-afstand", type=float, default=75)
    c.add_argument("--stad", help="Stad om mee te zoeken als naam + adres niets oplevert")
    args = ap.parse_args()
    return {"zoek": cmd_zoek, "rond": cmd_rond, "check": cmd_check}[args.cmd](args)


if __name__ == "__main__":
    sys.exit(main())
