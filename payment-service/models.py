from pydantic import BaseModel
from typing import Optional


class Payment(BaseModel):
    id: int
    booking_id: int
    amount: float
    payment_method: str
    payment_status: str
    payment_date: str


class PaymentCreate(BaseModel):
    booking_id: int
    amount: float
    payment_method: str
    payment_status: str
    payment_date: str


class PaymentUpdate(BaseModel):
    booking_id: Optional[int] = None
    amount: Optional[float] = None
    payment_method: Optional[str] = None
    payment_status: Optional[str] = None
    payment_date: Optional[str] = None