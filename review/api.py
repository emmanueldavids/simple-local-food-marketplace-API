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

review_router = APIRouter()
models.Base.metadata.create_all(bind=engine)



# Pydantic models
class ReviewBase(BaseModel):
    customer_id: int
    product_id: int
    farmer_id: int
    rating: int
    comment: str



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
@review_router.post("/", response_model=ReviewBase)
async def create_review(review: ReviewBase, db: db_dependency):
    db_review = models.Review(customer_id=review.customer_id, product_id=review.product_id, farmer_id=review.farmer_id, rating=review.rating, comment=review.comment)
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


# List all orders
@review_router.get('/', status_code=status.HTTP_200_OK)
async def get_user(db: db_dependency):
    review = db.query(models.Review).all()
    if review is None:
        raise HTTPException(status_code=404, detail='Review Not Found')
    return review


# Get Order by ID
@review_router.get('/review/{review_id}', status_code=status.HTTP_200_OK)
async def get_user(review_id: int,db: db_dependency):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()
    if review is None:
        raise HTTPException(status_code=404, detail='Review Not Found')
    return review
