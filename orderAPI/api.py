from enum import Enum
from msilib import schema
from fastapi import APIRouter, HTTPException, Response, Request, Depends,status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Annotated
import datetime
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

order_router = APIRouter()
models.Base.metadata.create_all(bind=engine)


class OrderStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# Pydantic models
class OrderBase(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    total: float
    status: int


#dependency for the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


#----------START ORDER API---------------

# Create Order
@order_router.post("/", response_model=OrderBase)
async def create_order(order: OrderBase, db: db_dependency):
    db_order = models.Order(customer_id=order.customer_id, product_id=order.product_id, quantity=order.quantity, total=order.total, status=order.status)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


# List all orders
@order_router.get('/', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency):
    orders = db.query(models.Order).all()
    if orders is None:
        raise HTTPException(status_code=404, detail='Order Not Found')
    return orders


# Get Order by ID
@order_router.get('/order/{order_id}', status_code=status.HTTP_200_OK)
async def get_user(order_id: int,db: db_dependency):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='Order Not Found')
    return order


# # Get task by due date
# @order_router.get("/tasks/due_date/{task_due_date}", status_code=status.HTTP_200_OK)
# async def task_due_date(tasks_due_date: datetime.date, db: db_dependency):
#     filtered_tasks = db.query(models.Tasks).filter(models.Tasks.id == tasks_due_date).first()
#     if not filtered_tasks:
#         raise HTTPException(status_code=404, detail="No Due Date found for the specified due date")
#     return filtered_tasks


# Update Order
@order_router.put('/order/{order_id}', status_code=status.HTTP_200_OK)
async def update_order(order_id: int, order: OrderBase, db: db_dependency):
    update_order = db.query(models.Order).filter((models.Order.id) == order_id).first()
    if update_order is None:
        raise HTTPException(status_code=404, detail='Order Not Found')
    
    update_order.quantity = order.quantity
    update_order.total = order.total
    
    db.commit()
    return update_order


# to Delete Order by id
@order_router.delete('/order/{order_id}', status_code=status.HTTP_200_OK)
async def get_order(order_id: int, db: db_dependency):
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    if order is None:
        raise HTTPException(status_code=404, detail='Order Not Found')
    db.delete(order)
    db.commit()
    return "Order Deleted Successfull"

#------------------END OF Order API------------------------------------------
