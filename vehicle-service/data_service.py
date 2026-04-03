from models import Vehicle


class VehicleMockDataService:
    def __init__(self):
        self.vehicles = [
            Vehicle(
                id=1,
                customer_id=1,
                vehicle_number="CAB-1234",
                brand="Toyota",
                model="Prius",
                year=2020,
                fuel_type="Hybrid"
            ),
            Vehicle(
                id=2,
                customer_id=2,
                vehicle_number="KDH-5678",
                brand="Honda",
                model="Civic",
                year=2019,
                fuel_type="Petrol"
            )
        ]
        self.next_id = 3

    def get_all_vehicles(self):
        return self.vehicles

    def get_vehicle_by_id(self, vehicle_id: int):
        return next((v for v in self.vehicles if v.id == vehicle_id), None)

    def add_vehicle(self, vehicle_data):
        new_vehicle = Vehicle(id=self.next_id, **vehicle_data.dict())
        self.vehicles.append(new_vehicle)
        self.next_id += 1
        return new_vehicle

    def update_vehicle(self, vehicle_id: int, vehicle_data):
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if vehicle:
            update_data = vehicle_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(vehicle, key, value)
            return vehicle
        return None

    def delete_vehicle(self, vehicle_id: int):
        vehicle = self.get_vehicle_by_id(vehicle_id)
        if vehicle:
            self.vehicles.remove(vehicle)
            return True
        return False