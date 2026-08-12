# crud.py tesztek

from datetime import datetime

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import models, crud


# ---------- Előkészítés ----------

@pytest.fixture()
def db():
    """Minden teszt előtt friss, üres, memóriában lévő adatbázist ad."""
    engine = create_engine("sqlite:///:memory:")
    models.Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture()
def spot(db):
    """Egy sima, korlátozás nélküli, aktív parkolóhely."""
    s = models.ParkingSpot(code="A1", restriction=None, active=True)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@pytest.fixture()
def restricted_spot(db):
    """Egy korlátozott, csak 'mozgaskorlatozott' csoportnak elérhető hely."""
    s = models.ParkingSpot(code="B1", restriction="mozgaskorlatozott", active=True)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


@pytest.fixture()
def inactive_spot(db):
    """Egy inaktív hely, amire nem lehet foglalni."""
    s = models.ParkingSpot(code="C1", restriction=None, active=False)
    db.add(s)
    db.commit()
    db.refresh(s)
    return s


# ---------- 1. Sikeres foglalás sima helyre ----------

def test_sikeres_foglalas_sima_helyre(db, spot):
    reservation = crud.create_reservation(
        db,
        spot_id=spot.id,
        requester="Kovács Anna",
        requester_group=None,
        start_time=datetime(2026, 8, 20, 9, 0),
        end_time=datetime(2026, 8, 20, 11, 0),
    )

    assert reservation.id is not None
    assert reservation.status == models.ReservationStatus.CONFIRMED


# ---------- 2. Ütköző foglalás elutasítása ----------

def test_utkozo_foglalas_elutasitasa(db, spot):
    crud.create_reservation(
        db,
        spot_id=spot.id,
        requester="Első kérelmező",
        requester_group=None,
        start_time=datetime(2026, 8, 20, 9, 0),
        end_time=datetime(2026, 8, 20, 11, 0),
    )

    with pytest.raises(ValueError):
        crud.create_reservation(
            db,
            spot_id=spot.id,
            requester="Második kérelmező",
            requester_group=None,
            start_time=datetime(2026, 8, 20, 10, 0),   # átfed az elsővel
            end_time=datetime(2026, 8, 20, 12, 0),
        )


# ---------- 3. Nem ütköző foglalások elfogadása ----------

def test_nem_utkozo_foglalasok_elfogadasa(db, spot):
    elso = crud.create_reservation(
        db,
        spot_id=spot.id,
        requester="Első kérelmező",
        requester_group=None,
        start_time=datetime(2026, 8, 20, 9, 0),
        end_time=datetime(2026, 8, 20, 10, 0),
    )

    masodik = crud.create_reservation(
        db,
        spot_id=spot.id,
        requester="Második kérelmező",
        requester_group=None,
        start_time=datetime(2026, 8, 20, 10, 0),   # csak azután kezdődik, hogy az első véget ért
        end_time=datetime(2026, 8, 20, 11, 0),
    )

    assert elso.id is not None
    assert masodik.id is not None


# ---------- 4. Korlátozott helyre jogosult kérelmező átmegy ----------

def test_korlatozott_helyre_jogosult_kerelmezo_atmegy(db, restricted_spot):
    reservation = crud.create_reservation(
        db,
        spot_id=restricted_spot.id,
        requester="Nagy Béla",
        requester_group="mozgaskorlatozott",   # egyezik a hely restriction mezőjével
        start_time=datetime(2026, 8, 20, 9, 0),
        end_time=datetime(2026, 8, 20, 10, 0),
    )

    assert reservation.id is not None
    assert reservation.status == models.ReservationStatus.CONFIRMED


# ---------- 5. Korlátozott helyre nem jogosult kérelmező elutasítva ----------

def test_korlatozott_helyre_nem_jogosult_elutasitva(db, restricted_spot):
    with pytest.raises(ValueError):
        crud.create_reservation(
            db,
            spot_id=restricted_spot.id,
            requester="Kiss Erik",
            requester_group="altalanos",   # nem egyezik a hely restriction mezőjével
            start_time=datetime(2026, 8, 20, 9, 0),
            end_time=datetime(2026, 8, 20, 10, 0),
        )


# ---------- 6. Inaktív helyre nem lehet foglalni ----------

def test_inaktiv_helyre_nem_lehet_foglalni(db, inactive_spot):
    with pytest.raises(ValueError):
        crud.create_reservation(
            db,
            spot_id=inactive_spot.id,
            requester="Teszt Elemér",
            requester_group=None,
            start_time=datetime(2026, 8, 20, 9, 0),
            end_time=datetime(2026, 8, 20, 10, 0),
        )


# ---------- 7. Lemondás után ugyanarra az időszakra újra lehet foglalni ----------

def test_lemondas_utan_ujra_foglalhato_ugyanarra_az_idoszakra(db, spot):
    start = datetime(2026, 8, 20, 9, 0)
    end = datetime(2026, 8, 20, 10, 0)

    elso = crud.create_reservation(
        db,
        spot_id=spot.id,
        requester="Első kérelmező",
        requester_group=None,
        start_time=start,
        end_time=end,
    )

    crud.cancel_reservation(db, elso.id)
    db.refresh(elso)
    assert elso.status == models.ReservationStatus.CANCELLED

    masodik = crud.create_reservation(
        db,
        spot_id=spot.id,
        requester="Második kérelmező",
        requester_group=None,
        start_time=start,   # pontosan ugyanaz az időszak, mint az elsőé
        end_time=end,
    )

    assert masodik.id is not None
    assert masodik.status == models.ReservationStatus.CONFIRMED