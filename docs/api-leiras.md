# API-leírás — Parkolóhely-foglalás

Elérés: `http://localhost:8000`
Kipróbálható felület: `http://localhost:8000/docs`

---

## GET /parking-spots
Visszaadja az összes parkolóhelyet.

Példa válasz:
```json
[
  { "id": 1, "code": "A-01", "restriction": null, "active": true }
]
```

---

## GET /parking-spots/{spot_id}/reservations
Egy adott hely foglalásait adja vissza.

---

## POST /reservations
Új foglalás létrehozása.

Amit el kell küldeni:
```json
{
  "spot_id": 1,
  "requester": "Kovács János",
  "requester_group": null,
  "start_time": "2026-09-01T10:00:00",
  "end_time": "2026-09-01T12:00:00"
}
```

- `spot_id`, `requester`, `start_time`, `end_time` kötelező
- `requester_group` csak korlátozott helynél kell, és egyeznie kell a hely korlátozásával

Ha minden rendben, 201-es választ kapunk a létrehozott foglalással.

Hiba esetén:
- 422 → hibás adat (pl. a vég korábbi, mint a kezdet)
- 400 → nincs ilyen hely / foglalt az időszak / nem jogosult a helyre

---

## DELETE /reservations/{reservation_id}
Lemondja a foglalást (nem törli, csak "cancelled" állapotba teszi).