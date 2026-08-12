



| # | Döntési pont | Amit választottam                                                                    | Miért                                                                                                                                                                                                                                                                                                                                                                     | Milyen alternatívát vetettem el |
|---|---|--------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|---|
| 1 | Hogyan tudjuk meg, hogy egy hely szabad-e | Nem tárolom külön, hanem mindig a foglalásokból számolom ki                          | Ha külön tárolnám, két helyen lenne ugyanaz az infó, és könnyen szétcsúszhatnának egymástól                                                                                                                                                                                                                                                                               | Egy is_free igaz/hamis mező a parkolóhelyen, amit kézzel írogatnék át foglaláskor és lemondáskor |
| 2 | A requester_group mező kötelező legyen-e minden foglalásnál | Opcionális (nullable=True) — csak korlátozott helyeknél van jelentősége              | Ha kötelezővé tenném, minden foglalónak ki kellene találnia valamilyen csoportot még általános helyeknél is, ami felesleges, értelmetlen adatot eredményezne                                                                                                                                                                                                              | Kötelezővé tenni minden foglalásnál, függetlenül attól, hogy a hely korlátozott-e |
| 3 | Hol ellenőrizzük, hogy az end_time később van-e, mint a start_time | A schemas.py-ban, egy validáló függvénnyel, még mielőtt a kérés eljutna a crud.py-ig | Ez egy más jellegű ellenőrzés, mint az ütközés-vizsgálat: nem két különböző foglalást hasonlít össze, hanem azt nézi, hogy az egy bejövő kérés önmagában értelmes-e (a kezdete korábbi-e, mint a vége). Ha csak az ütközés-ellenőrzésre hagyatkoznék, egy visszafelé menő időintervallum (pl. 15:00–10:00) simán átmenne egy üres adatbázisnál, mert nincs mivel ütköznie | Nem külön ellenőrizni, csak az ütközés-vizsgálatra hagyatkozni a crud.py-ban — ez hibás lett volna, mert nem fogja meg az önmagában is értelmetlen (visszafelé menő) időintervallumokat |

#### 1: Megnézzük a Reservation táblát
Megkeressük: van-e olyan sor, ahol spot_id = az A-01 hely azonosítója, ÉS status = "confirmed" (aktív, nem lemondott), ÉS a kérdéses időpont a start_time és end_time közé esik
Ha találunk ilyen sort → a hely foglalt
Ha nem találunk → a hely szabad

A fejlesztés során a legnagyobb nehézséget az okozta, hogy eldöntsem, 
egy-egy ellenőrzés melyik fájlba tartozik, ahogyan pl. a start_time 
és end_time sorrendjének vizsgálata az adatbázis-logikát tartalmazó 
crud.py-ba kerüljön, vagy inkább a bejövő adatok ellenőrzését 
elvégző schemas.py-ba. A megoldás egyszerű volt hiszen az egyik a request értelmezhetőségét, 
a másik az ütközés logikáját vizsgálta.

A másik hibám vagy nehézségem az volt, hogy elkerüljem a felesleges
adattárolást: pl.: hogy ne tároljak külön mezőt arról, hogy egy 
parkolóhely szabad-e, hanem ezt mindig a foglalásokból számoljam ki. 
Végül úgy düntöttem, hogy jobb, ha egy adatot nem tárolunk 
külön, hanem igény szerint kiszámoljuk a már meglévő adatokból.