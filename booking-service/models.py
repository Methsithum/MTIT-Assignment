from pydantic import BaseModel
from typing import Optional


class Booking(BaseModel):
    id: int
    customer_id: int
    vehicle_id: int
    service_type: str
    booking_date: str
    booking_time: str
    status: str


class BookingCreate(BaseModel):
    customer_id: int
    vehicle_id: int
    service_type: str
    booking_date: str
    booking_time: str
    status: str


class BookingUpdate(BaseModel):
    customer_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    service_type: Optional[str] = None
    booking_date: Optional[str] = None
    booking_time: Optional[str] = None
    status: Optional[str] = None