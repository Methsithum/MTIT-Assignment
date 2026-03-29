from data_service import BookingMockDataService


class BookingService:
    def __init__(self):
        self.data_service = BookingMockDataService()

    def get_all(self):
        return self.data_service.get_all_bookings()

    def get_by_id(self, booking_id: int):
        return self.data_service.get_booking_by_id(booking_id)

    def create(self, booking_data):
        return self.data_service.add_booking(booking_data)

    def update(self, booking_id: int, booking_data):
        return self.data_service.update_booking(booking_id, booking_data)

    def delete(self, booking_id: int):
        return self.data_service.delete_booking(booking_id)