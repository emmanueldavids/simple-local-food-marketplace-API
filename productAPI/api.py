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

product_router = APIRouter()
models.Base.metadata.create_all(bind=engine)


# Pydantic models
class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    category: str
    farmer_id: int


#dependency for the database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


#----------START PRODUCT API---------------

# Create product
@product_router.post("/", response_model=ProductBase)
async def create_product(product: ProductBase, db: db_dependency):
    db_product = models.Product(name=product.name, description=product.description, price=product.price, category=product.category, farmer_id=product.farmer_id)
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


# List all Products
@product_router.get('/', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency):
    product = db.query(models.Product).all()
    if product is None:
        raise HTTPException(status_code=404, detail='Product Not Found')
    return product


# Get Product by ID
@product_router.get('/product/{product_id}', status_code=status.HTTP_200_OK)
async def get_user(product_id: int,db: db_dependency):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product Not Found')
    return product


# # Get task by due date
# @product_router.get("/tasks/due_date/{task_due_date}", status_code=status.HTTP_200_OK)
# async def task_due_date(tasks_due_date: datetime.date, db: db_dependency):
#     filtered_tasks = db.query(models.Tasks).filter(models.Tasks.id == tasks_due_date).first()
#     if not filtered_tasks:
#         raise HTTPException(status_code=404, detail="No Due Date found for the specified due date")
#     return filtered_tasks


# Update Product
@product_router.put('/product/{product_id}', status_code=status.HTTP_200_OK)
async def update_product(product_id: int, product: ProductBase, db: db_dependency):
    update_product = db.query(models.Product).filter((models.Product.id) == product_id).first()
    if update_product is None:
        raise HTTPException(status_code=404, detail='Product Not Found')
    
    update_product.name = product.name
    update_product.description = product.description
    
    db.commit()
    return update_product


# to Delete Product by id
@product_router.delete('/product/{product_id}', status_code=status.HTTP_200_OK)
async def get_product(product_id: int, db: db_dependency):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if product is None:
        raise HTTPException(status_code=404, detail='Product Not Found')
    db.delete(product)
    db.commit()
    return "Product Deleted Successfull"

#------------------END OF Product API------------------------------------------
