from fastapi import FastAPI, HTTPException, status
from models import Customer, CustomerCreate, CustomerUpdate
from service import CustomerService
from typing import List

app = FastAPI(title="Customer Microservice", version="1.0.0")

customer_service = CustomerService()


@app.get("/")
def read_root():
    return {"message": "Customer Microservice is running"}


@app.get("/api/customers", response_model=List[Customer])
def get_all_customers():
    return customer_service.get_all()


@app.get("/api/customers/{customer_id}", response_model=Customer)
def get_customer(customer_id: int):
    customer = customer_service.get_by_id(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer


@app.post("/api/customers", response_model=Customer, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate):
    return customer_service.create(customer)


@app.put("/api/customers/{customer_id}", response_model=Customer)
def update_customer(customer_id: int, customer: CustomerUpdate):
    updated_customer = customer_service.update(customer_id, customer)
    if not updated_customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    return updated_customer


@app.delete("/api/customers/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int):
    success = customer_service.delete(customer_id)
    if not success:
        raise HTTPException(status_code=404, detail="Customer not found")
    return None