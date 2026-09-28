#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["pyyaml"]
# ///
"""Bundel een reis tot één markdown-bestand voor de web/app-versie van Claude of ChatGPT.

Voice mode onderweg heeft geen toegang tot de vault. Dit script zet alles wat een
gids onderweg nodig heeft in één plat bestand zonder wikilinks: instructies voor de
assistent, het reisprofiel (alleen de relevante secties), het routedocument en per
plek adres, coördinaten, Maps-link en beschrijving.

Gebruik:
  export_onderweg.py "<pad of naam van Trip-notitie>" [--vault PAD] [--zakelijk]

Uitvoer: <vault>/reisgids-export/<Trip> - onderweg.md
Dat pad synct via Obsidian naar de telefoon, zodat je het daar aan een project hangt.
"""

import argparse
import os
import re
import sys
from datetime import date
from pathlib import Path

import yaml

SOORTEN = {
    "utensils": "eten/drinken", "coffee": "koffie/bakkerij/ijs", "shopping-basket": "markt",
    "landmark": "bezienswaardigheid", "mountain": "natuur/uitzicht", "waves": "strand/zwemplek",
    "bed": "verblijf", "car": "parkeren/vervoer", "shopping-bag": "winkel", "briefcase": "afspraak/zakelijk",
}

WIKILINK = re.compile(r"!?\[\[([^\]|#]*)(?:#([^\]|]*))?(?:\|([^\]]+))?\]\]")


def split_fm(text: str) -> tuple[dict, str]:
    if text.startswith("---"):
        _, fm, body = text.split("---", 2)
        return (yaml.safe_load(fm) or {}), body.strip()
    return {}, text.strip()


def plat(text: str) -> str:
    """Wikilinks naar platte tekst; embeds (zoals de Trips.base-view) weg."""
    text = re.sub(r"!\[\[[^\]]+\]\]", "", text)
    text = WIKILINK.sub(lambda m: m.group(3) or m.group(1).split("/")[-1] or m.group(2), text)
    text = re.sub(r"^## Trips\s*$", "", text, flags=re.M)
    return re.sub(r"\n{3,}", "\n\n", text).strip()


def linknaam(v) -> str | None:
    m = WIKILINK.search(str(v))
    return m.group(1).split("/")[-1].strip() if m and m.group(1) else None


def index(vault: Path) -> dict[str, Path]:
    """Notitienaam en aliases → pad, zoals Obsidian links oplost."""
    idx: dict[str, Path] = {}
    for p in vault.rglob("*.md"):
        if any(part.startswith(".") for part in p.relative_to(vault).parts):
            continue
        idx.setdefault(p.stem, p)
    for p in (vault / "3_Resources/Places").glob("*.md"):
        fm, _ = split_fm(p.read_text(encoding="utf-8"))
        for a in fm.get("aliases") or []:
            idx.setdefault(str(a), p)
    return idx


def profiel_secties(vault: Path, zakelijk: bool) -> str:
    p = vault / "2_Areas/Reizen/Reisprofiel.md"
    if not p.exists():
        return ""
    _, body = split_fm(p.read_text(encoding="utf-8"))
    secties = re.split(r"(?m)^(?=## )", body)
    # Zakenreis: kind en vakantie-logistiek zijn ruis. Vakantie: de zakelijke regels.
    skip = {"## Wie er reist", "## Met kind", "## Vakantie", "## Hoe een plan eruitziet"} if zakelijk else {"## Zakenreis", "## Hoe een plan eruitziet"}
    keep = [s for s in secties if s.startswith("## ") and s.splitlines()[0].strip() not in skip]
    tekst = "\n".join(keep)
    return plat(tekst)


def reislog_sectie() -> str:
    """Het reislog-formaat uit references/reislog-formaat.md, de enige bron ervan.

    Voice mode kan niet in de vault schrijven; daarom vragen we hem het reislog als
    tekst te geven in een vast formaat, dat stap 9 van de skill weer inleest.
    """
    p = Path(__file__).resolve().parent.parent / "references" / "reislog-formaat.md"
    if not p.exists():
        return ""
    tekst = p.read_text(encoding="utf-8")
    formaat = re.search(r"## Het formaat\s+(```markdown\n.*?```)", tekst, re.S)
    regels = re.search(r"## Regels, en waarom\s+(.*?)(?=\n## |\Z)", tekst, re.S)
    if not formaat:
        return ""
    return (
        "## Reislog bijhouden\n\n"
        "Onthoud tijdens het gesprek waar we geweest zijn, wat we gegeten hebben, wat we willen onthouden en wat "
        "we ervan leerden. Zeggen we \"reislog\" of \"dagafsluiting\", geef dan het reislog van die dag als "
        "Markdown in precies dit formaat, zonder inleiding of afsluiting eromheen, zodat we het in één keer "
        "kunnen kopiëren. Lees het in voice mode niet voor: zeg alleen dat het klaarstaat in de tekst.\n\n"
        + formaat.group(1)
        + ("\n\n" + regels.group(1).strip() if regels else "")
    )


def plek(p: Path) -> str:
    fm, body = split_fm(p.read_text(encoding="utf-8"))
    c = fm.get("coordinates") or []
    regels = [f"### {p.stem}"]
    soort = SOORTEN.get(fm.get("icon"), fm.get("icon") or "")
    if soort:
        regels.append(f"- Soort: {soort}")
    if fm.get("address"):
        regels.append(f"- Adres: {fm['address']}")
    if fm.get("rating"):
        r = f"{float(fm['rating']):g}".replace(".", ",")
        regels.append(f"- Onze rating: {r} van 5 sterren" + (f" (laatst bezocht {fm['last']})" if fm.get("last") else ""))
    if len(c) == 2:
        regels.append(f"- Coördinaten: {c[0]}, {c[1]}")
        regels.append(f"- Navigeren: https://www.google.com/maps/dir/?api=1&destination={c[0]},{c[1]}")
    if fm.get("source"):
        regels.append(f"- Google Maps: {fm['source']}")
    body = re.sub(r"(?m)^Onderdeel van \[\[.*\]\]\.?\s*$", "", body)  # staat al in de route
    if b := plat(body):
        regels.append("\n" + b)
    return "\n".join(regels)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("trip")
    ap.add_argument("--vault", default=os.environ.get("VAULT"), required="VAULT" not in os.environ)
    ap.add_argument("--zakelijk", action="store_true", help="Zakenreis: laat vakantie- en kind-secties weg")
    a = ap.parse_args()

    vault = Path(a.vault).expanduser()
    idx = index(vault)
    trip = Path(a.trip)
    if not trip.exists():
        trip = idx.get(Path(a.trip).stem) or sys.exit(f"Trip-notitie niet gevonden: {a.trip}")
    fm, body = split_fm(trip.read_text(encoding="utf-8"))

    plekken, missend = [], []
    for v in fm.get("loc") or []:
        n = linknaam(v)
        (plekken if n in idx else missend).append(idx.get(n, n))

    # Alleen reisdocumenten (route, voorbereiding); een beursnotitie of taak hoort niet in de gids
    docs = [
        idx[n]
        for v in fm.get("related_notes") or []
        if (n := linknaam(v)) in idx and idx[n].is_relative_to(vault / "2_Areas/Reizen")
    ]

    delen = [
        f"# {trip.stem} – reisgids onderweg",
        f"_Gegenereerd {date.today().isoformat()} uit de Obsidian-vault. Dit bestand is de enige bron; de vault zelf is onderweg niet bereikbaar._",
        "## Instructies voor de assistent\n\n"
        + ("Je bent mijn reisgids tijdens deze zakenreis. Ik praat vaak via voice mode, onderweg, met weinig tijd.\n\n" if a.zakelijk else
           "Je bent onze reisgids tijdens deze reis. We praten vaak via voice mode, onderweg, met weinig tijd.\n\n") +
        "- Antwoord kort en spreekbaar: eerst het advies, dan hooguit twee zinnen uitleg. Geen tabellen of lange lijsten voorlezen\n"
        "- Gebruik de plekken en de route hieronder als eerste bron. Noem de plek bij naam zodat we hem in de lijst terugvinden\n"
        "- Vraag je om iets dat hier niet in staat (een apotheek, een alternatief restaurant), zeg dan dat het een nieuwe suggestie is en noem een plek die je zeker weet; bij twijfel liever zoeken dan gokken\n"
        "- Houd rekening met het profiel en met de uitgangspunten van deze reis (wie er reist, dieetwensen) in het routedocument; vraag die niet opnieuw\n"
        "- Openingstijden en drukte veranderen; zeg het als iets gecontroleerd moet worden",
    ]
    if log := reislog_sectie():
        delen.append(log)
    if prof := profiel_secties(vault, a.zakelijk):
        delen.append("## Over ons (reisprofiel)\n\n" + re.sub(r"(?m)^## ", "### ", prof))
    reis = [f"- Start: {fm.get('start') or '?'}", f"- Eind: {fm.get('end') or '?'}"]
    if b := plat(body):
        reis.append("\n" + b)
    delen.append("## De reis\n\n" + "\n".join(reis))
    for d in docs:
        _, db = split_fm(d.read_text(encoding="utf-8"))
        db = re.sub(r"(?m)\A# .*\n?", "", plat(db)).strip()  # eigen H1 weg, de sectiekop vervangt hem
        delen.append(f"## {d.stem}\n\n" + re.sub(r"(?m)^(#+) ", r"#\1 ", db))
    if plekken:
        delen.append("## Plekken\n\n" + "\n\n".join(plek(p) for p in plekken))

    out_dir = vault / "reisgids-export"
    out_dir.mkdir(parents=True, exist_ok=True)
    out = out_dir / f"{trip.stem} - onderweg.md"
    out.write_text("\n\n".join(delen) + "\n", encoding="utf-8")

    print(out)
    print(f"{len(plekken)} plekken, {len(docs)} routedocument(en)")
    if missend:
        print("NIET GEVONDEN in de vault:", ", ".join(missend))
    return 0


if __name__ == "__main__":
    sys.exit(main())
