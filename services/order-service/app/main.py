from fastapi import FastAPI
from pydantic import BaseModel
from typing import List


app = FastAPI(
    title="ShopSphere Order Service",
    description="Order management service for ShopSphere DevSecOps Platform",
    version="0.1.0",
)


class OrderItem(BaseModel):
    product_id: int
    product_name: str
    quantity: int
    unit_price: int


class CreateOrderRequest(BaseModel):
    user_id: int
    items: List[OrderItem]


ORDERS = []


@app.get("/")
def root():
    return {
        "service": "order-service",
        "message": "ShopSphere Order Service is running",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "order-service",
    }


@app.get("/orders")
def get_orders():
    return {
        "items": ORDERS,
        "total": len(ORDERS),
    }


@app.get("/orders/{order_id}")
def get_order_by_id(order_id: int):
    for order in ORDERS:
        if order["id"] == order_id:
            return order

    return {
        "error": "Order not found",
        "order_id": order_id,
    }


@app.post("/orders")
def create_order(request: CreateOrderRequest):
    total_amount = 0

    for item in request.items:
        total_amount += item.quantity * item.unit_price

    new_order = {
        "id": len(ORDERS) + 1,
        "user_id": request.user_id,
        "items": [item.model_dump() for item in request.items],
        "total_amount": total_amount,
        "status": "created",
    }

    ORDERS.append(new_order)

    return new_order


@app.patch("/orders/{order_id}/status")
def update_order_status(order_id: int, status: str):
    for order in ORDERS:
        if order["id"] == order_id:
            order["status"] = status
            return order

    return {
        "error": "Order not found",
        "order_id": order_id,
    }