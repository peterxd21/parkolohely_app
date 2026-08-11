# Adatbázis-modellek: ORM altal itt megirt kod a tuloldalon eletbe lep
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import enum



class ParkingSpot(Base):
    __tablename__ = "parking_spots"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(20), unique=True, nullable=False)
    restriction = Column(String(50), nullable=True)
    active = Column(Boolean, nullable=False, default=True)

    reservations = relationship("Reservation", back_populates="spot")

class ReservationStatus(str, enum.Enum):
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class Reservation(Base):
    __tablename__ = "reservations"

    id = Column(Integer, primary_key=True, index=True)
    spot_id = Column(Integer, ForeignKey("parking_spots.id"), nullable=False)
    requester = Column(String(100), nullable=False)
    requester_group = Column(String(50), nullable=True)
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    status = Column(Enum(ReservationStatus), nullable=False, default=ReservationStatus.CONFIRMED)

    spot = relationship("ParkingSpot", back_populates="reservations")


