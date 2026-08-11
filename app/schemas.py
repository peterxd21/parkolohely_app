from datetime import datetime
from pydantic import BaseModel, field_validator


class ReservationCreate(BaseModel):
    spot_id: int
    requester: str
    requester_group: str | None = None
    start_time: datetime
    end_time: datetime

    @field_validator("end_time")
    @classmethod
    def end_time_kesobb_legyen(cls, end_time, info):
        start_time = info.data.get("start_time")
        if start_time is not None and end_time <= start_time:
            raise ValueError("end_time-nek később kell lennie, mint start_time")
        return end_time


