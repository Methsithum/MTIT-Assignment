from data_service import PaymentMockDataService


class PaymentService:
    def __init__(self):
        self.data_service = PaymentMockDataService()

    def get_all(self):
        return self.data_service.get_all_payments()

    def get_by_id(self, payment_id: int):
        return self.data_service.get_payment_by_id(payment_id)

    def create(self, payment_data):
        return self.data_service.add_payment(payment_data)

    def update(self, payment_id: int, payment_data):
        return self.data_service.update_payment(payment_id, payment_data)