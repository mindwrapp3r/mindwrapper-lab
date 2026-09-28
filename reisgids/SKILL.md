---
name: reisgids
description: >-
  Persoonlijke reisgids voor een reiziger of gezin. Plant zakenreizen, vakanties,
  stedentrips en dagtrips in de Obsidian-vault — Places-notities met gecontroleerde
  coördinaten, één routedocument, een Trip-notitie met `loc:` — en maakt een export voor
  voice mode onderweg in de Claude- of ChatGPT-app. Gebruik deze skill ALTIJD zodra een
  reis, trip, uitje, weekendje weg of zakenreis ter sprake komt: plannen, restaurants of
  bezienswaardigheden zoeken, een wandelroute maken, "wat moeten we zien in X", "waar kunnen
  we eten in X", parkeren in een stad, een dagtrip vanaf een verblijf, plekken toevoegen aan
  de kaart, of een reis klaarzetten voor onderweg. Ook bij het evalueren van een reis
  achteraf (reisverslag → reisprofiel bijwerken), en bij een reislog of dagafsluiting uit voice
  mode dat in de vault verwerkt moet worden. Triggers: "reis plannen", "trip",
  "zakenreis", "vakantie", "dagtrip", "stedentrip", "wandelroute", "reisgids", "plaatsen
  toevoegen", "places", "export voor onderweg", "voice mode reis", "reisprofiel", "reislog", "dagafsluiting",
  "reislog verwerken".
---

# Reisgids

Een reisplan dat past bij wie er reist, in de vault staat als plekken op de kaart, en onderweg via voice mode bereikbaar is. De web-versies van Claude en ChatGPT konden dat al redelijk (Málaga, sept 2026), maar kenden het gezin niet, controleerden coördinaten niet, zagen bestaande plekken niet en vulden de Trip-koppeling niet. Die vier dingen zijn waar deze skill het verschil maakt.

**Vault:** je Obsidian-vault; `export_onderweg.py` neemt `--vault` of de omgevingsvariabele `VAULT`. De mappen hieronder (`2_Areas/Reizen/`, `3_Resources/Places/`, `Template/`) zijn een voorbeeldindeling: pas ze aan op je eigen vault.
**Scripts:** `scripts/` naast dit bestand, dus `~/.claude/skills/reisgids/scripts/`. Roep ze met het volledige pad aan; het zijn UV-scripts.
Schrijf alle markdown zonder harde regelafbrekingen binnen een alinea — Obsidian toont elke newline.

## 1. Context laden

Lees eerst `2_Areas/Reizen/Reisprofiel.md`. Daarin staat wie er reist, wat een reis goed maakt, wat tegenvalt, en aparte regels voor vakantie en zakenreis. Alles wat je voorstelt moet daartegen kloppen; een generieke top-10 is precies wat we niet willen.

Stel dan vast (vraag alleen wat je niet uit het verzoek kunt halen, in één vraagronde):
- **Soort reis:** zakenreis, vakantie, stedentrip of dagtrip. Zakenreis = tijd boven geld, maar niet onnodig duur
- **Datum/data en tijdvak:** aankomsttijd, hoeveel uur er is
- **Wie gaat er mee.** Gaat er een kind mee? Reken dan de leeftijd uit **op de reisdatum** en lees de sectie "Met kind": ervaringen zijn met leeftijd genoteerd omdat ze verlopen. Wat bij 8 maanden gold (draagzak, eten om 18:00) kan met 2 jaar anders zijn
- **Zakenreis:** vraag naar dieetwensen — die bepalen alle eetsuggesties
- **Vervoer:** auto (parkeren nodig), OV, te voet

## 2. Kijken wat er al is

- **Plekken:** zoek in `3_Resources/Places/` op plaatsnaam, adres en aliases (`grep -ril "<stad>" 3_Resources/Places`). Een bestaande plek hergebruik je en link je; je maakt nooit een tweede notitie voor dezelfde plek. Zie je een dubbele, meld het
- **Reizen:** `2_Areas/Reizen/` bevat reisverslagen en voorbereidingsnotities. Bestaat er al een reisverslag voor deze reis, dan is dát de Trip-notitie (zie stap 6); een voorbereidingsnotitie (vluchtgegevens, checklist) blijft voorbereiding en verwijst ernaar
- **Eerdere bezoeken:** noemt het profiel deze stad of streek, gebruik die ervaring. Places-notities van eerdere reizen in dezelfde streek zijn kandidaten om opnieuw te noemen. `rating:` beslist: 4–5 noem je opnieuw ("vorige keer 5 sterren"), 3 alleen als het goed uitkomt, 1–2 raad je af. Ook de ratings elders zeggen iets: welke soort plek scoort hoog (markthal, familierestaurant) en welke laag

## 2b. Leren van eerdere reizen

Het profiel is een samenvatting en loopt altijd iets achter. De bron zijn de reisverslagen: elke Trip-notitie in `2_Areas/Reizen/` (`grep -l '"\[\[Trips\]\]"' 2_Areas/Reizen/*.md`). De reizigers schrijven daarin vaak kopjes als *Leermomenten*, *Wat ging goed*, *Aanvulling* of een evaluatie aan het eind.

- Lees in elk geval de verslagen die nieuwer zijn dan `updated:` van het profiel, plus die van hetzelfde soort reis (zaken of vakantie) of dezelfde streek
- Zoek wat van toepassing is op déze reis: praktische lessen (eigen risico afkopen, documenten in Obsidian), ontdekkingen (een plek, een gerecht, een aanpak die werkte) en patronen (ruzie bij lange autoritten, te veel eten)
- Geef ze als tips: een kopje *💡 Uit eerdere reizen* in het routedocument, en noem de twee of drie belangrijkste kort in de chat. Verwijs naar het verslag waar de tip uit komt, zodat hij te herleiden is
- Staat een les nog niet in het profiel, stel dan voor om hem toe te voegen (zie stap 9)

## 3. Onderzoeken en voorstellen

Zoek op het web naar actuele informatie. Goede bronnen zijn lokale foodblogs, recente reviews en officiële sites; controleer openingsdagen (markten zijn vaak alleen 's ochtends of op vaste dagen, siësta, maandag dicht). Kies weinig en goed: een handvol plekken die echt bij ons passen, met per plek waarom.

Voor een dagtrip of korte route kun je direct doorschrijven. Bij een langere reis of als er echte keuzes zijn: leg eerst een korte shortlist en een routeschets voor in de chat, en schrijf de notities na akkoord — twintig notities die weggegooid worden kosten meer dan één vraag.

## 4. Places-notities

Pad: `3_Resources/Places/<Naam>.md`. Gebruik als naam de naam zoals hij op borden en Google Maps staat (`Mercado de Atarazanas`); een Nederlandse of alternatieve naam gaat in `aliases`, net als de officiële langere naam. Aliases helpen ook de coördinatencontrole.

Frontmatter volgt `Template/Plaats template.md`, zonder de Templater-regels:

```yaml
---
created: YYYY-MM-DD
categories:
  - "[[Places]]"
source: 'https://www.google.com/maps/search/?api=1&query=<naam+adres, url-encoded>'
tags:
  - places
icon: utensils
color: orange
coordinates:
  - "36.7184080"
  - "-4.4240607"
address: "Calle Atarazanas 10, Centro Histórico, 29005 Málaga, Spanje"
rating:
last:
aliases:
  - "Mercado Central de Atarazanas"
---
<1–3 zinnen: wat het is en waarom het bij ons past. Praktische tip (wanneer gaan, wat bestellen, reserveren).>

Onderdeel van [[<routedocument>]].

## Trips

![[Trips.base#Locatie]]
```

- **Coördinaten** haal je op met `geocode.py zoek "<naam>, <stad>"` en schrijf je met 7 decimalen, als strings. Neem ze niet uit je geheugen: de web-versie van Claude zat in Málaga 90–120 m naast drie restaurants. Vindt `zoek` een zaak niet, dan heet hij in OSM vaak net anders (Casa Montaña = "Bodega Montaña"): gebruik `geocode.py rond "<deel van naam>" --bij <lat,lon van de buurt> --straal 1000`. Controleer altijd of het type klopt (`amenity/restaurant`, niet `highway/...`)
- **Parkeergarage:** het punt is de **auto-inrit**, want daar navigeer je naartoe. Zoek die met `geocode.py rond "<naam>|parking" --bij ...`; inritten staan in OSM als `amenity=parking_entrance`
- **Plek in een plek** (een bar in een markthal, een kraam): eigen notitie als het een bestemming op zich is, met de coördinaten van de ingang van het gebouw en in de tekst waar hij binnen zit
- **Afspraak of klant zonder bekend adres:** vraag het adres; is het er niet, maak de notitie met `briefcase` en het punt van de omgeving, en zet bovenaan de tekst dat het adres nog ingevuld moet worden
- **Plan B krijgt ook een notitie** (parkeren, restaurant): hij hoort in `loc:` en moet onderweg in de export staan, juist als plan A tegenvalt
- **`rating` en `last`** blijven leeg bij het plannen: alleen de reizigers zelf geven een rating, na een bezoek (stap 9). Methode van kepano: `rating` is een getal (1 tot 5, halve sterren mogen: `4.5`), `last` de datum van het laatste bezoek; de view *Ratings* in `Places.base` toont ze als sterren (★★★★½) en sorteert erop
- **Adres** volledig, inclusief postcode en stad — het script zoekt daar de stad in terug
- **`## Trips` met de embed** moet erin; daardoor verschijnt de reis onderaan de plek zodra de Trip-notitie `loc:` gevuld heeft

Icoon en kleur per soort (Lucide-iconen), zodat de kaart in één oogopslag leesbaar is. `Places.base` en `Map.base` lezen `icon` en `color` rechtstreeks uit de notitie; kleur is een CSS-kleurnaam:

| Soort | icon | color |
|---|---|---|
| Restaurant, tapasbar, bodega | `utensils` | orange |
| Koffie, bakkerij, ijs | `coffee` | orange |
| Markt, markthal | `shopping-basket` | orange |
| Bezienswaardigheid, kerk, fort, plein | `landmark` | red |
| Natuur, uitzicht, wandeling | `mountain` | green |
| Strand, zwemplek | `waves` | teal |
| Verblijf, hotel | `bed` | purple |
| Parkeren, station, vervoer | `car` | blue |
| Winkel, pottenbakker | `shopping-bag` | pink |
| Afspraak, klant, beurs | `briefcase` | gray |

## 5. Routedocument

Eén document per reis (of per dag bij een meerdaagse reis) in `2_Areas/Reizen/`, naam `YYYY <Bestemming> - <onderwerp>.md`, bijvoorbeeld `2026 Malaga - wandelroute centrum.md`. Dit format werkte het best en is het voorbeeld om te volgen:

```markdown
---
created: YYYY-MM-DD
related_notes:
  - "[[<Trip-notitie>]]"
tags:
  - reizen
---
# <Bestemming> – <onderwerp>

Geplande aankomst: **rond 11:00 uur**.

## 🧭 Uitgangspunten  ← wie reist er mee (kind: leeftijd op reisdatum), dieetwensen, vervoer, harde tijden. Zo hoeft de gids onderweg niet opnieuw te vragen
## 🕘 Tijdschema       ← alleen bij harde tijden (afspraak, vlucht): opsomming "09:30 landen", geen tabel — voice mode leest het voor
## 🚗 Parkeren          ← of 🚆 Vervoer; altijd eerste keuze én plan B
## 🚶 Route            ← genummerd, elke stop een [[link]]
## 🍽️ Eten             ← per plek één regel waarom; lokale specialiteit noemen
## 📏 Afstand          ← kilometers en tijd, klimmetjes apart
## 💡 Praktisch        ← volgorde-redenen (markt 's ochtends), wat bewust is weggelaten, schoenen/water
## 💡 Uit eerdere reizen ← tips uit stap 2b, elk met [[bronverslag]]
```

Houd rekening met het profiel: met een kind een pauze- en dutjesmoment en een vroeg eetadres; in Spanje een plan B voor het late diner; bij hitte schaduw en airco.

## 6. Trip-notitie = het reisverslag

Het reisverslag ís de Trip-notitie: dezelfde notitie waarin de reiziger tijdens en na de reis schrijft, en die in `Trips.base` staat. Bestaat er al een verslag voor deze reis, gebruik dat. Anders maak je `2_Areas/Reizen/YYYY Reisverslag <Bestemming>.md` aan met een lege body, klaar om in te schrijven. Voorbereiding zoals vluchtgegevens en een checklist mag in een aparte notitie zonder `categories: [[Trips]]`, die via `related_notes` naar het verslag verwijst. Zo staat elke reis maar één keer in de base.

Frontmatter volgens `Template/Trip template.md`:

```yaml
---
created: YYYY-MM-DD
categories:
  - "[[Trips]]"
start: YYYY-MM-DD
end:
loc:
  - "[[Plek 1]]"
  - "[[Plek 2]]"
tags:
  - reizen
aliases:
related_notes:
  - "[[<routedocument>]]"
---
```

`loc:` bevat **alle** plekken van de reis, ook parkeren en eten; dat is wat `Trips.base` en de kaart voedt. Raak de body van een bestaand verslag niet aan — alleen de frontmatter.

## 7. Controleren

```bash
geocode.py check 3_Resources/Places/<Plek>.md [...]
```

Meldt per plek de afwijking in meters tegen OpenStreetMap, zoekt alleen binnen ~3 km van het eigen punt, en toont welke zoekvraag raak was en welk OSM-type terugkwam. Beoordeel met verstand:
- **`ok`** (≤ 75 m): goed
- **`AFWIJKING`** bij een straat, plein, park of groot complex (Calle Larios, Alcazaba): normaal, OSM geeft het midden. Controleer of jouw punt op de ingang of het begin ligt
- **`AFWIJKING`** bij een restaurant of winkel: vrijwel altijd fout. Zoek opnieuw met `zoek` op het adres; let op ketens met meerdere vestigingen (Casa Lola heeft er drie)
- **Circulair:** heb je de coördinaten zelf uit `zoek` op het adres gehaald, dan geeft `check` 0 m. Dat bewijst niets; kijk dan of het OSM-type bij de plek past
- **`NIET GEVONDEN`**: OSM kent de naam niet. Probeer `zoek` met het adres of de lokale naam; lukt het niet, laat de coördinaten staan en meld dat ze niet gecontroleerd zijn

## 8. Export voor onderweg

Onderweg heeft de app op de telefoon geen toegang tot de vault. Maak daarom één plat bestand:

```bash
scripts/export_onderweg.py "<Trip-notitie>" [--zakelijk]
```

Uitvoer: `reisgids-export/<Trip> - onderweg.md` — instructies voor de assistent, de relevante secties van het reisprofiel (bij `--zakelijk` zonder vakantie- en kind-deel), de route en per plek adres, coördinaten en een navigatielink. Het bestand synct via Obsidian naar de telefoon.

Vertel de gebruiker daarna:
1. Maak in de Claude- of ChatGPT-app een project voor deze reis en voeg dit bestand toe als projectkennis
2. Start voice mode vanuit dat project
3. Verandert het plan in de vault, draai de export opnieuw en vervang het bestand
4. Aan het eind van de dag "dagafsluiting" of "reislog" zeggen, en voor die ene vraag naar tekst gaan: het reislog komt als Markdown-blok dat de gebruiker naar Obsidian deelt (bijvoorbeeld in een inbox-map of onder het reisverslag). Het formaat staat in `references/reislog-formaat.md`; de export neemt het automatisch op

Eén markdown-bestand werkt betrouwbaarder dan een zip: niet elke app pakt een zip uit, en voice mode leest kennisbestanden niet altijd volledig in.

## 9. Na de reis

- **Reislog verwerken (eerst):** verzamel de reislogs van deze reis: blokken die de gebruiker uit de voice mode van ChatGPT of Claude heeft gedeeld en in de vault heeft gezet (bijvoorbeeld in een inbox-map of onder het reisverslag). Het formaat staat in `references/reislog-formaat.md`. Verwerk per regel:
  - **Plekken en Gegeten** → zoek de Places-notitie (stap 2); bestaat hij niet, maak hem (stap 4, met gecontroleerde coördinaten). `bezocht` → in `loc:` van de Trip-notitie en `last:` op de dag van het reislog; `idee` → niet in `loc:`, wel onder *Ideeën* in het verslag
  - **⭐ in het reislog** is een rating die de gebruiker zelf gaf: zet hem als voorstel in het ratinglijstje hieronder en laat hem bevestigen, want een voice-transcript kan een getal verkeerd verstaan
  - **Ideeën** en **Leermomenten** → onder die kopjes in de Trip-notitie (het reisverslag), met de datum erbij; leermomenten zijn ook de bron voor het profielvoorstel hieronder
  - Toon eerst in de chat wat je van plan bent (nieuwe Places, wijzigingen in `loc:`, ratings) en schrijf na akkoord. Verwerkte reislog-notities blijven staan; vraag of ze weg mogen

- **Locaties bijwerken:** plekken die in het verslag genoemd worden maar niet in `loc:` staan (een restaurant dat onderweg ontdekt is), krijgen een Places-notitie en gaan erbij. Vraag welke geplande plekken niet bezocht zijn; die mogen uit `loc:`, zodat de kaart laat zien waar we echt waren
- **Ratings:** vraag voor elke bezochte plek een rating van 1 tot 5 en zet `last:` op de bezoekdatum. Stel het als één lijstje dat de gebruiker snel kan invullen, met je eigen inschatting uit het verslag als voorzet ("La Picada: heerlijk gegeten → 4 of 5?"). Vul nooit zelf een rating in zonder akkoord. Halve sterren mogen (`4.5`). Schaal: 5 = uitstekend, zeker terug · 4 = goed, aanrader · 3 = prima, niet bijzonder · 2 = tegenvaller · 1 = nooit meer
- **Profiel bijwerken:** lees de leermomenten en evaluatie in het verslag en stel wijzigingen aan `Reisprofiel.md` voor — wat werkte, wat tegenviel, nieuwe ervaringen met het kind **met de leeftijd erbij**. Het profiel is één centrale pagina die je bijwerkt (en `updated:` ophoogt), geen plek om losse notities aan te hangen. Vraag akkoord voordat je wijzigt;
