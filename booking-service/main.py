from fastapi import FastAPI, HTTPException, status, Response
from models import Booking, BookingCreate, BookingUpdate
from service import BookingService
from typing import List, Dict, Any

app = FastAPI(title="Booking Microservice", version="1.0.0")

booking_service = BookingService()


@app.get("/")
def read_root():
    return {"message": "Booking Microservice is running"}


@app.get("/api/bookings")
def get_all_bookings():
    bookings = booking_service.get_all()
    return {
        "message": f"Successfully retrieved {len(bookings)} bookings",
        "data": bookings
    }


@app.get("/api/bookings/{booking_id}")
def get_booking(booking_id: int):
    booking = booking_service.get_by_id(booking_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {
        "message": f"Successfully retrieved booking with ID: {booking_id}",
        "data": booking
    }


@app.post("/api/bookings", status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, response: Response):
    created_booking = booking_service.create(booking)
    response.headers["X-Success-Message"] = "Booking created successfully"
    return {
        "message": "Booking created successfully",
        "data": created_booking
    }


@app.put("/api/bookings/{booking_id}")
def update_booking(booking_id: int, booking: BookingUpdate, response: Response):
    updated_booking = booking_service.update(booking_id, booking)
    if not updated_booking:
        raise HTTPException(status_code=404, detail="Booking not found")
    response.headers["X-Success-Message"] = f"Booking {booking_id} updated successfully"
    return {
        "message": f"Booking with ID {booking_id} updated successfully",
        "data": updated_booking
    }


@app.delete("/api/bookings/{booking_id}", status_code=status.HTTP_200_OK)
def delete_booking(booking_id: int, response: Response):
    success = booking_service.delete(booking_id)
    if not success:
        raise HTTPException(status_code=404, detail="Booking not found")
    response.headers["X-Success-Message"] = f"Booking {booking_id} deleted successfully"
    return {
        "message": f"Booking with ID {booking_id} deleted successfully",
        "success": True
    }