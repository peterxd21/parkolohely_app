# Ez a fájl köti össze a rétegeket: HTTP végpontok (route-ok)

from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, engine, Base
from app import models, schemas, crud
from app.seed import seed_ha_ures

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_ha_ures(db)
    finally:
        db.close()
    yield


app = FastAPI(title="Parkolóhely-foglalás API", lifespan=lifespan)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/parking-spots", response_model=list[schemas.ParkingSpotOut])
def get_parking_spots(db: Session = Depends(get_db)):
    return crud.list_spots(db)


@app.get("/parking-spots/{spot_id}/reservations", response_model=list[schemas.ReservationOut])
def get_spot_reservations(spot_id: int, db: Session = Depends(get_db)):
    return crud.list_reservations_for_spot(db, spot_id)


@app.post("/reservations", response_model=schemas.ReservationOut, status_code=201)
def create_reservation(payload: schemas.ReservationCreate, db: Session = Depends(get_db)):
    try:
        return crud.create_reservation(
            db,
            spot_id=payload.spot_id,
            requester=payload.requester,
            requester_group=payload.requester_group,
            start_time=payload.start_time,
            end_time=payload.end_time,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.delete("/reservations/{reservation_id}", response_model=schemas.ReservationOut)
def cancel_reservation(reservation_id: int, db: Session = Depends(get_db)):
    try:
        return crud.cancel_reservation(db, reservation_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
