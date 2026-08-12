#Tesztek a bemeneti validáláshoz (schemas.py)

from datetime import datetime

import pytest
from pydantic import ValidationError

from app import schemas


# ---------- Érvénytelen időszak: a vég korábbi, mint a kezdet ----------

def test_vege_korabbi_mint_kezdet_elutasitva():
    with pytest.raises(ValidationError):
        schemas.ReservationCreate(
            spot_id=1,
            requester="Teszt Elemér",
            requester_group=None,
            start_time=datetime(2026, 8, 20, 12, 0),
            end_time=datetime(2026, 8, 20, 9, 0),   # korábbi, mint a start_time
        )


# ---------- Érvénytelen időszak: a vég pontosan megegyezik a kezdettel ----------

def test_vege_egyenlo_kezdettel_elutasitva():
    with pytest.raises(ValidationError):
        schemas.ReservationCreate(
            spot_id=1,
            requester="Teszt Elemér",
            requester_group=None,
            start_time=datetime(2026, 8, 20, 9, 0),
            end_time=datetime(2026, 8, 20, 9, 0),   # nulla hosszúságú időszak
        )


# ---------- Érvényes időszak: a vég később van, mint a kezdet ----------

def test_ervenyes_idoszak_elfogadva():
    reservation = schemas.ReservationCreate(
        spot_id=1,
        requester="Teszt Elemér",
        requester_group=None,
        start_time=datetime(2026, 8, 20, 9, 0),
        end_time=datetime(2026, 8, 20, 10, 0),
    )

    assert reservation.start_time < reservation.end_time