from models import Customer


class CustomerMockDataService:
    def __init__(self):
        self.customers = [
            Customer(
                id=1,
                name="Nimal Perera",
                email="nimal@example.com",
                phone="0711234567",
                address="Colombo"
            ),
            Customer(
                id=2,
                name="Kasun Silva",
                email="kasun@example.com",
                phone="0779876543",
                address="Kandy"
            )
        ]
        self.next_id = 3

    def get_all_customers(self):
        return self.customers

    def get_customer_by_id(self, customer_id: int):
        return next((c for c in self.customers if c.id == customer_id), None)

    def add_customer(self, customer_data):
        new_customer = Customer(id=self.next_id, **customer_data.dict())
        self.customers.append(new_customer)
        self.next_id += 1
        return new_customer

    def update_customer(self, customer_id: int, customer_data):
        customer = self.get_customer_by_id(customer_id)
        if customer:
            update_data = customer_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(customer, key, value)
            return customer
        return None

    def delete_customer(self, customer_id: int):
        customer = self.get_customer_by_id(customer_id)
        if customer:
            self.customers.remove(customer)
            return True
        return False