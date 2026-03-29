from models import Booking


class BookingMockDataService:
    def __init__(self):
        self.bookings = [
            Booking(
                id=1,
                customer_id=1,
                vehicle_id=1,
                service_type="Oil Change",
                booking_date="2026-03-30",
                booking_time="10:00 AM",
                status="Pending"
            ),
            Booking(
                id=2,
                customer_id=2,
                vehicle_id=2,
                service_type="Full Service",
                booking_date="2026-03-31",
                booking_time="02:00 PM",
                status="Confirmed"
            )
        ]
        self.next_id = 3

    def get_all_bookings(self):
        return self.bookings

    def get_booking_by_id(self, booking_id: int):
        return next((b for b in self.bookings if b.id == booking_id), None)

    def add_booking(self, booking_data):
        new_booking = Booking(id=self.next_id, **booking_data.dict())
        self.bookings.append(new_booking)
        self.next_id += 1
        return new_booking

    def update_booking(self, booking_id: int, booking_data):
        booking = self.get_booking_by_id(booking_id)
        if booking:
            update_data = booking_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(booking, key, value)
            return booking
        return None

    def delete_booking(self, booking_id: int):
        booking = self.get_booking_by_id(booking_id)
        if booking:
            self.bookings.remove(booking)
            return True
        return False