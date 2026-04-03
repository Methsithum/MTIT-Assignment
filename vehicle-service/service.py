from data_service import VehicleMockDataService


class VehicleService:
    def __init__(self):
        self.data_service = VehicleMockDataService()

    def get_all(self):
        return self.data_service.get_all_vehicles()

    def get_by_id(self, vehicle_id: int):
        return self.data_service.get_vehicle_by_id(vehicle_id)

    def create(self, vehicle_data):
        return self.data_service.add_vehicle(vehicle_data)

    def update(self, vehicle_id: int, vehicle_data):
        return self.data_service.update_vehicle(vehicle_id, vehicle_data)

    def delete(self, vehicle_id: int):
        return self.data_service.delete_vehicle(vehicle_id)