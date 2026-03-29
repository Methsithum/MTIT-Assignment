from fastapi import FastAPI, HTTPException, status
from models import Payment, PaymentCreate, PaymentUpdate
from service import PaymentService
from typing import List

app = FastAPI(title="Payment Microservice", version="1.0.0")

payment_service = PaymentService()


@app.get("/")
def read_root():
    return {"message": "Payment Microservice is running"}


@app.get("/api/payments", response_model=List[Payment])
def get_all_payments():
    return payment_service.get_all()


@app.get("/api/payments/{payment_id}", response_model=Payment)
def get_payment(payment_id: int):
    payment = payment_service.get_by_id(payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


@app.post("/api/payments", response_model=Payment, status_code=status.HTTP_201_CREATED)
def create_payment(payment: PaymentCreate):
    return payment_service.create(payment)


@app.put("/api/payments/{payment_id}", response_model=Payment)
def update_payment(payment_id: int, payment: PaymentUpdate):
    updated_payment = payment_service.update(payment_id, payment)
    if not updated_payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return updated_payment