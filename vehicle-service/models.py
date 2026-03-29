from pydantic import BaseModel
from typing import Optional


class Vehicle(BaseModel):
    id: int
    customer_id: int
    vehicle_number: str
    brand: str
    model: str
    year: int
    fuel_type: str


class VehicleCreate(BaseModel):
    customer_id: int
    vehicle_number: str
    brand: str
    model: str
    year: int
    fuel_type: str


class VehicleUpdate(BaseModel):
    customer_id: Optional[int] = None
    vehicle_number: Optional[str] = None
    brand: Optional[str] = None
    model: Optional[str] = None
    year: Optional[int] = None
    fuel_type: Optional[str] = None