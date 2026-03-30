from fastapi import FastAPI, HTTPException, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import httpx
import jwt
from datetime import datetime, timedelta
import logging
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("api_gateway")

app = FastAPI(title="API Gateway", version="1.0.0")

SERVICES = {
    "customer": "http://localhost:8001",
    "vehicle": "http://localhost:8002",
    "booking": "http://localhost:8003",
    "payment": "http://localhost:8004"
}

SECRET_KEY = "super-secret-key-change-in-production-2026"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()


class LoginRequest(BaseModel):
    username: str
    password: str


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return token
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@app.post("/token")
async def login(data: LoginRequest):
    if data.username == "admin" and data.password == "admin123":
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        token = jwt.encode(
            {"sub": data.username, "exp": expire},
            SECRET_KEY,
            algorithm=ALGORITHM
        )
        return {"access_token": token, "token_type": "bearer"}

    raise HTTPException(status_code=401, detail="Incorrect username or password")


@app.middleware("http")
async def logging_middleware(request: Request, call_next):
    logger.info(f"→ {request.method} {request.url.path}")
    start = datetime.now()
    response = await call_next(request)
    duration = (datetime.now() - start).total_seconds() * 1000
    logger.info(f"← {response.status_code} {request.method} {request.url.path} ({duration:.2f}ms)")
    return response


@app.exception_handler(HTTPException)
async def custom_http_exception(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
            "method": request.method,
            "detail": exc.detail
        }
    )


@app.exception_handler(Exception)
async def generic_exception(request: Request, exc: Exception):
    logger.error(f"Unhandled error at {request.url.path}: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "timestamp": datetime.utcnow().isoformat(),
            "path": request.url.path,
            "detail": "Internal gateway error – check logs"
        }
    )


async def forward_request(service: str, path: str, method: str, **kwargs) -> Any:
    if service not in SERVICES:
        raise HTTPException(status_code=404, detail="Service not found")

    url = f"{SERVICES[service]}{path}"

    async with httpx.AsyncClient() as client:
        try:
            if method == "GET":
                response = await client.get(url, **kwargs)
            elif method == "POST":
                response = await client.post(url, **kwargs)
            elif method == "PUT":
                response = await client.put(url, **kwargs)
            elif method == "DELETE":
                response = await client.delete(url, **kwargs)
            else:
                raise HTTPException(status_code=405, detail="Method not allowed")

            try:
                content = response.json()
            except ValueError:
                content = response.text if response.text else None

            if response.status_code == 204:
                return JSONResponse(status_code=204, content=None)

            return JSONResponse(content=content, status_code=response.status_code)

        except httpx.RequestError as e:
            logger.error(f"Service {service} unavailable: {e}")
            raise HTTPException(status_code=503, detail=f"Service unavailable: {str(e)}")
        except Exception as e:
            logger.error(f"Gateway error forwarding to {url}: {e}")
            raise HTTPException(status_code=502, detail=f"Bad gateway: {str(e)}")


@app.get("/")
def read_root():
    return {
        "message": "API Gateway is running",
        "available_services": list(SERVICES.keys())
    }


# Customer routes
@app.get("/gateway/customers")
async def get_all_customers(token: str = Depends(verify_token)):
    return await forward_request("customer", "/api/customers", "GET")


@app.get("/gateway/customers/{customer_id}")
async def get_customer(customer_id: int, token: str = Depends(verify_token)):
    return await forward_request("customer", f"/api/customers/{customer_id}", "GET")


@app.post("/gateway/customers")
async def create_customer(request: Request, token: str = Depends(verify_token)):
    body = await request.json()
    return await forward_request("customer", "/api/customers", "POST", json=body)


@app.put("/gateway/customers/{customer_id}")
async def update_customer(customer_id: int, request: Request, token: str = Depends(verify_token)):
    body = await request.json()
    return await forward_request("customer", f"/api/customers/{customer_id}", "PUT", json=body)


@app.delete("/gateway/customers/{customer_id}")
async def delete_customer(customer_id: int, token: str = Depends(verify_token)):
    return await forward_request("customer", f"/api/customers/{customer_id}", "DELETE")


# Vehicle routes
@app.get("/gateway/vehicles")
async def get_all_vehicles(token: str = Depends(verify_token)):
    return await forward_request("vehicle", "/api/vehicles", "GET")


@app.get("/gateway/vehicles/{vehicle_id}")
async def get_vehicle(vehicle_id: int, token: str = Depends(verify_token)):
    return await forward_request("vehicle", f"/api/vehicles/{vehicle_id}", "GET")


@app.post("/gateway/vehicles")
async def create_vehicle(request: Request, token: str = Depends(verify_token)):
    body = await request.json()
    return await forward_request("vehicle", "/api/vehicles", "POST", json=body)


@app.put("/gateway/vehicles/{vehicle_id}")
async def update_vehicle(vehicle_id: int, request: Request, token: str = Depends(verify_token)):
    body = await request.json()
    return await forward_request("vehicle", f"/api/vehicles/{vehicle_id}", "PUT", json=body)


@app.delete("/gateway/vehicles/{vehicle_id}")
async def delete_vehicle(vehicle_id: int, token: str = Depends(verify_token)):
    return await forward_request("vehicle", f"/api/vehicles/{vehicle_id}", "DELETE")


# Booking routes
@app.get("/gateway/bookings")
async def get_all_bookings(token: str = Depends(verify_token)):
    return await forward_request("booking", "/api/bookings", "GET")


@app.get("/gateway/bookings/{booking_id}")
async def get_booking(booking_id: int, token: str = Depends(verify_token)):
    return await forward_request("booking", f"/api/bookings/{booking_id}", "GET")


@app.post("/gateway/bookings")
async def create_booking(request: Request, token: str = Depends(verify_token)):
    body = await request.json()
    return await forward_request("booking", "/api/bookings", "POST", json=body)


@app.put("/gateway/bookings/{booking_id}")
async def update_booking(booking_id: int, request: Request, token: str = Depends(verify_token)):
    body = await request.json()
    return await forward_request("booking", f"/api/bookings/{booking_id}", "PUT", json=body)


@app.delete("/gateway/bookings/{booking_id}")
async def delete_booking(booking_id: int, token: str = Depends(verify_token)):
    return await forward_request("booking", f"/api/bookings/{booking_id}", "DELETE")


# Payment routes
@app.get("/gateway/payments")
async def get_all_payments(token: str = Depends(verify_token)):
    return await forward_request("payment", "/api/payments", "GET")


@app.get("/gateway/payments/{payment_id}")
async def get_payment(payment_id: int, token: str = Depends(verify_token)):
    return await forward_request("payment", f"/api/payments/{payment_id}", "GET")


@app.post("/gateway/payments")
async def create_payment(request: Request, token: str = Depends(verify_token)):
    body = await request.json()
    return await forward_request("payment", "/api/payments", "POST", json=body)


@app.put("/gateway/payments/{payment_id}")
async def update_payment(payment_id: int, request: Request, token: str = Depends(verify_token)):
    body = await request.json()
    return await forward_request("payment", f"/api/payments/{payment_id}", "PUT", json=body)