## Parkolóhely-foglalás backend

-- A rendszer egy Rest api-t biztosít a parkolóhelyek nyilvántartására és foglalására.


### Használt technológiák: 
- Python (FastAPI) 
- MySQL (SQLAlchemy ORM) 
- Docker 


### Adatmodell / Adattárolás:
 
#### ParkingSpot (parkolóhelyek)
| Mező | Típus | Leírás |
|---|---|---|
| id | INT, PK | Egyedi azonosító, automatikusan generált |
| code | VARCHAR(20), UNIQUE | Emberi olvasható azonosító (pl A-1) |
| restriction | VARCHAR(50), NULL | Ha kitöltött, a hely korlátozott használatú (pl. "mozgaskorlatozott"). Ha üres, bárki foglalhatja. |
| active | BOOLEAN | Kikapcsolható, ha egy hely átmenetileg nem foglalható |


#### Reservation (foglalások)

| Mező | Típus | Leírás |
|---|---|---|
| id | INT, PK | Egyedi azonosító, automatikusan generált |
| spot_id | INT, FK → parking_spots.id | Melyik parkolóhelyre szól a foglalás |
| requester | VARCHAR(100) | Kérelmező neve/azonosítója |
| requester_group | VARCHAR(50), NULL | Kérelmező csoportja — korlátozott helyeknél ennek egyeznie kell a hely `restriction` mezőjével |
| start_time | DATETIME | Foglalás kezdete |
| end_time | DATETIME | Foglalás vége |
| status | ENUM('confirmed', 'cancelled') | Foglalás állapota |

## 3. Kapcsolat a két tábla között

Egy ParkingSpot-nak több "Reservation"-je lehet (idővel, egymás
után), de egy Reservation pontosan egy ParkingSpot-hoz
tartozik. Ezt a spot_id idegen kulcs (foreign key) valósítja meg,
ami a Reservation táblában a ParkingSpot tábla id-jára mutat.

## 4. Szabályok 

- Egy parkolóhelyen két aktív (confirmed) foglalás nem fedheti
  át egymást időben.
- Ha egy hely restriction mezője ki van töltve, csak az foglalhatja,
  akinek a requester_group-ja pontosan egyezik vele.
- Lemondás esetén a foglalás rekordja megmarad, csak a status vált
  cancelled-re 

 