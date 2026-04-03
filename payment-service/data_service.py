from models import Payment


class PaymentMockDataService:
    def __init__(self):
        self.payments = [
            Payment(
                id=1,
                booking_id=1,
                amount=5000.00,
                payment_method="Cash",
                payment_status="Paid",
                payment_date="2026-03-25"
            ),
            Payment(
                id=2,
                booking_id=2,
                amount=7500.00,
                payment_method="Card",
                payment_status="Pending",
                payment_date="2026-03-26"
            )
        ]
        self.next_id = 3

    def get_all_payments(self):
        return self.payments

    def get_payment_by_id(self, payment_id: int):
        return next((p for p in self.payments if p.id == payment_id), None)

    def add_payment(self, payment_data):
        new_payment = Payment(id=self.next_id, **payment_data.dict())
        self.payments.append(new_payment)
        self.next_id += 1
        return new_payment

    def update_payment(self, payment_id: int, payment_data):
        payment = self.get_payment_by_id(payment_id)
        if payment:
            update_data = payment_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(payment, key, value)
            return payment
        return None