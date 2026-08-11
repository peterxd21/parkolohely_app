| # | Döntési pont | Amit választottam | Miért | Milyen alternatívát vetettem el                                                                  |
|---|---|---|---|--------------------------------------------------------------------------------------------------|
| 1 | Hogyan tudjuk meg, hogy egy hely szabad-e | Nem tárolom külön, hanem mindig a foglalásokból számolom ki | Ha külön tárolnám, két helyen lenne ugyanaz az infó, és könnyen szétcsúszhatnának egymástól | Egy is_free igaz/hamis mező a parkolóhelyen, amit kézzel írogatnék át foglaláskor és lemondáskor |


Megnézzük a Reservation táblát
Megkeressük: van-e olyan sor, ahol spot_id = az A-01 hely azonosítója, ÉS status = "confirmed" (aktív, nem lemondott), ÉS a kérdéses időpont a start_time és end_time közé esik
Ha találunk ilyen sort → a hely foglalt
Ha nem találunk → a hely szabad