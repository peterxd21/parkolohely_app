# Felhasználói kézikönyv — Parkolóhely-foglalás

## Mi ez?

Egy program, amivel parkolóhelyeket lehet lekérdezni és lefoglalni. Nincs hozzá saját ablak/képernyő — böngészőben, egy kattintható felületen (/docs) lehet kipróbálni, vagy más programokból (pl. curl-lel) elérhető.

## Indítás

Szükséges hozzá: Docker.

docker-compose up

Ez elindítja a teljes rendszert (adatbázis + program), és automatikusan feltölti 8 kezdő parkolóhellyel.

Pár másodperc múlva elérhető itt: http://localhost:8000/docs

Leállítás: Ctrl+C

## Használat

### Milyen helyek vannak?

Nyissa meg a /docs oldalt, kattintson a GET /parking-spots sorra, majd "Try it out" → "Execute". Megjelenik az összes hely, és látható, melyik korlátozott (pl. mozgáskorlátozott).

### Foglalás egy általános helyre

POST /reservations → "Try it out" → írja be:

{
  "spot_id": 1,
  "requester": "A neve",
  "requester_group": null,
  "start_time": "2026-09-01T10:00:00",
  "end_time": "2026-09-01T12:00:00"
}

→ "Execute"

Ha sikerült, a válasz tartalmaz egy foglalás-azonosítót (id) — ezt érdemes megjegyezni, ha később le kívánja mondani a foglalást.

### Foglalás korlátozott helyre

Ugyanez, de meg kell adni a requester_group mezőt, aminek egyeznie kell a hely korlátozásával (pl. "mozgaskorlatozott"). Ha nem egyezik, a rendszer elutasítja a kérést.

### Foglalás lemondása

DELETE /reservations/{reservation_id} → adja meg az azonosítót → "Execute". A foglalás nem törlődik, csak "lemondott" állapotba kerül.

## Gyakori hibák

| Hiba | Ok | Mit lehet tenni |
|---|---|---|
| A hely foglalt | Ütközik egy meglévő foglalással | Válasszon másik időpontot vagy helyet |
| Nem jogosult | A hely korlátozott, rossz csoport | Adja meg a megfelelő requester_group értéket |
| Nincs ilyen hely | Rossz spot_id | Nézze meg a /parking-spots listát |