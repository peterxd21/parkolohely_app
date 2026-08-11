# Kezdő referenciaadatok betöltése induláskor, Ez fogja feltölteni a kezdő parkolóhelyeket, amikor a rendszer először elindu

from sqlalchemy.orm import Session
from app import models

KEZDO_HELYEK = [
    {"code": "A-01", "restriction": None},
    {"code": "A-02", "restriction": None},
    {"code": "A-03", "restriction": None},
    {"code": "B-01", "restriction": "mozgaskorlatozott"},
    {"code": "B-02", "restriction": "mozgaskorlatozott"},
    {"code": "C-01", "restriction": "elektromos_tolto"},
    {"code": "C-02", "restriction": "elektromos_tolto"},
    {"code": "D-01", "restriction": "lakossagi"},
]


def seed_ha_ures(db: Session):
    letezo_darabszam = db.query(models.ParkingSpot).count()
    if letezo_darabszam > 0:
        return

    for hely_adat in KEZDO_HELYEK:
        uj_hely = models.ParkingSpot(**hely_adat, active=True)
        db.add(uj_hely)
    db.commit()