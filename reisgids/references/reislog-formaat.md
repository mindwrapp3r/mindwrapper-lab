# Reislog-formaat

Eén vast formaat voor wat er onderweg gebeurt, zodat het na afloop zonder giswerk in de vault terechtkomt (stap 9 van de skill). Het wordt op twee plekken gebruikt, en beide lezen deze beschrijving:

- **De export voor onderweg** (`export_onderweg.py`) zet het formaat in de instructies voor de voice mode van ChatGPT of Claude. Die kan niet in de vault schrijven, dus hij geeft het reislog als tekst op "reislog" of "dagafsluiting"
- **Stap 9, "reislog verwerken"**, leest het weer in

Een reislog is een verslag van wat de reiziger heeft verteld, geen samenvatting van wat de assistent heeft voorgesteld. Een plek komt erin als de reiziger er geweest is of hem wil onthouden, niet omdat de assistent hem noemde.

## Het formaat

```markdown
## Reislog <dag> <DD-MM-YYYY> – <reis>

### Plekken
- **<Naam zoals op Google Maps>** · <plaats of adres> · bezocht | idee · ⭐ <1–5, alleen als de reiziger hem gaf> · <één zin: waarom, voor wie, wat opviel>

### Gegeten
- **<Naam>** · <plaats> · ⭐ <1–5, alleen als de reiziger hem gaf> · <wat, en of het met kinderen werkte>

### Ideeën voor een volgende keer
- <iets wat bleef hangen maar niet gedaan is, met plaats>

### Leermomenten
- <wat werkte of tegenviel, zo concreet mogelijk; bij een kind met de leeftijd erbij>
```

## Regels, en waarom

- **Een kopje zonder inhoud laat je weg.** Een lege sectie leest bij het verwerken als "hier is niets gebeurd", terwijl er gewoon niets over is gezegd
- **⭐ alleen als de reizigers hem zelf noemden** ("dat was echt een vier"). De skill vult nooit zelf een rating in zonder akkoord, en een rating van de assistent zou bij het verwerken niet meer van een echte te onderscheiden zijn. Geen rating genoemd: dan het ⭐-veld weglaten
- **Naam zoals op Google Maps** (bijvoorbeeld "Kinderboerderij Samenzóo", niet "die kinderboerderij"), plus plaats. Daarmee vindt stap 9 een bestaande Places-notitie terug of maakt hij er een die de coördinatencontrole doorstaat
- **Onzeker is onzeker.** Komt een tijd of prijs van internet en is hij niet nagekeken, zet er "(niet nagekeken)" achter
- **Eén reislog per dag.** Meerdere dagen in één gesprek: één blok per dag, onder elkaar
- **Geen codes, telefoonnummers of adressen van mensen** in het reislog; het wordt gekopieerd en gedeeld

## Voorbeeld

```markdown
## Reislog dinsdag 12-05-2026 – 2026 voorbeeldreis Overijssel

### Plekken
- **Weekmarkt Ommen** · Markt, Ommen · bezocht · ⭐ 4 · gezellig en niet te druk, de peuter keek z'n ogen uit naar de kramen
- **Kinderboerderij Samenzóo** · Staphorst · idee · voor op de terugweg, openingstijden nog nakijken

### Gegeten
- **Pannenkoekenhuis De Kiepe** · Ommen · ⭐ 3 · prima, kinderstoel was er, wel lang wachten

### Leermomenten
- Markt vóór tienen bezoeken: daarna werd het te druk voor de buggy (peuter van 12 maanden)
```
