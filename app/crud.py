# ez a reteg dolgozik az adatbazissal / jogosultsag ellenorzes
from sqlalchemy.orm import Session
from app import models

def van_e_utkozes(db: Session, spot_id: int, start_time, end_time) -> bool:
    utkozo_foglalas = (
        db.query(models.Reservation)
        .filter(
            models.Reservation.spot_id == spot_id,
            models.Reservation.status == models.ReservationStatus.CONFIRMED,
            models.Reservation.start_time < end_time,
            models.Reservation.end_time > start_time,  # start time az uj foglalase. pl. ha valaki akar foglalni  11kor, de az elozo 13kor er veget akkor 13>11 es ezert nem elfogadhato.
        )
        .first()
    )
    return utkozo_foglalas is not None

def get_active_spot(db: Session, spot_id: int) -> models.ParkingSpot:
    spot = db.query(models.ParkingSpot).filter(models.ParkingSpot.id == spot_id).first()
    if spot is None:
        raise ValueError(f"Nincs ilyen parkolóhely: id={spot_id}")
    if not spot.active:
        raise ValueError(f"A parkolóhely ({spot.code}) jelenleg nem aktív")
    return spot

def create_reservation(db: Session, spot_id: int, requester: str, requester_group: str, start_time, end_time) -> models.Reservation:
    spot = get_active_spot(db, spot_id)

    if spot.restriction and requester_group != spot.restriction:
        raise ValueError(
            f"A(z) {spot.code} hely korlátozott ('{spot.restriction}'), "
            f"a kérelmező csoportja ('{requester_group}') nem jogosult rá."
        )

    if van_e_utkozes(db, spot_id, start_time, end_time):
        raise ValueError(f"A(z) {spot.code} hely már foglalt ebben az időszakban.")

    uj_foglalas = models.Reservation(
        spot_id=spot_id,
        requester=requester,
        requester_group=requester_group,
        start_time=start_time,
        end_time=end_time,
        status=models.ReservationStatus.CONFIRMED,
    )
    db.add(uj_foglalas)
    db.commit()
    db.refresh(uj_foglalas)
    return uj_foglalas

def cancel_reservation(db: Session, reservation_id: int) -> models.Reservation:
    foglalas = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if foglalas is None:
        raise ValueError(f"Nincs ilyen foglalás: id={reservation_id}")
    if foglalas.status == models.ReservationStatus.CANCELLED:
        raise ValueError(f"A(z) {reservation_id} foglalás már le van mondva.")

    foglalas.status = models.ReservationStatus.CANCELLED
    db.commit()
    db.refresh(foglalas)
    return foglalas


def list_spots(db: Session):
    return db.query(models.ParkingSpot).all()


def list_reservations_for_spot(db: Session, spot_id: int):
    return (
        db.query(models.Reservation)
        .filter(models.Reservation.spot_id == spot_id)
        .all()
    )