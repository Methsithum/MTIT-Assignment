from fastapi import FastAPI, HTTPException, status
from models import Vehicle, VehicleCreate, VehicleUpdate
from service import VehicleService
from typing import List

app = FastAPI(title="Vehicle Microservice", version="1.0.0")

vehicle_service = VehicleService()


@app.get("/")
def read_root():
    return {"message": "Vehicle Microservice is running"}


@app.get("/api/vehicles", response_model=List[Vehicle])
def get_all_vehicles():
    return vehicle_service.get_all()


@app.get("/api/vehicles/{vehicle_id}", response_model=Vehicle)
def get_vehicle(vehicle_id: int):
    vehicle = vehicle_service.get_by_id(vehicle_id)
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return vehicle


@app.post("/api/vehicles", response_model=Vehicle, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle: VehicleCreate):
    return vehicle_service.create(vehicle)


@app.put("/api/vehicles/{vehicle_id}", response_model=Vehicle)
def update_vehicle(vehicle_id: int, vehicle: VehicleUpdate):
    updated_vehicle = vehicle_service.update(vehicle_id, vehicle)
    if not updated_vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return updated_vehicle


@app.delete("/api/vehicles/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle(vehicle_id: int):
    success = vehicle_service.delete(vehicle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return None