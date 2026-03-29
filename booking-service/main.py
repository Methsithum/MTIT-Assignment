from fastapi import FastAPI, HTTPException, status
from models import Booking, BookingCreate, BookingUpdate
from service import BookingService
from typing import List

app = FastAPI(title="Booking Microservice", version="1.0.0")

booking_service = BookingService()


@app.get("/")
def read_root():
    return {"message": "Booking Microservice is running"}


@app.get("/api/bookings", response_model=List[Booking])
def get_all_bookings():
    return booking_service.get_all()


@app.get("/api/bookings/{booking_id}", response_model=Booking)
def get_booking(booking_id: int):
    booking = booking_service.get_by_id(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return booking


@app.post("/api/bookings", response_model=Booking, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate):
    return booking_service.create(booking)


@app.put("/api/bookings/{booking_id}", response_model=Booking)
def update_booking(booking_id: int, booking: BookingUpdate):
    updated_booking = booking_service.update(booking_id, booking)
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return updated_booking


@app.delete("/api/bookings/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: int):
    success = booking_service.delete(booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    return None