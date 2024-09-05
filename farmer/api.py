from fastapi import APIRouter, HTTPException, Response, Request, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import models
from typing import List, Annotated
from database import engine, SessionLocal
from sqlalchemy.orm import Session


farmer_router = APIRouter()
models.Base.metadata.create_all(bind=engine)



# Pydantic models
class FarmerBase(BaseModel):
    name: str
    username: str
    email: str
    password: str
    farm_name: str
    location: str


# class UserInBase(BaseModel):
#     username: str
#     email: str
#     password: str

# class UserOutBase(BaseModel):
#     id: int
#     username: str
#     email: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


# OAuth2 password bearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#Post user (Create User)
@farmer_router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(farm: FarmerBase, db: db_dependency):
    new_user = models.Farmer(name=farm.name, username=farm.username, email=farm.email, password=farm.password, farm_name=farm.farm_name, location=farm.location)
    db.add(new_user)
    db.commit()
    return new_user

#Get all user
@farmer_router.get("/", status_code=status.HTTP_200_OK)
async def read_users(db: db_dependency):
    users = db.query(models.Farmer).all()
    return users

#Get user by id
@farmer_router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.Farmer).filter((models.Farmer.id) == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Post Users Login
@farmer_router.post("/token", status_code=status.HTTP_201_CREATED)
async def login( db: db_dependency, form_data: OAuth2PasswordRequestForm = Depends()):
    user = db.query(models.Farmer).filter(models.Farmer.username == form_data.username).first()
    if not user or user.password != form_data.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return {"access_token": user.username, "token_type": "bearer"}

# Update User
@farmer_router.put('/{user_id}', status_code=status.HTTP_200_OK)
async def update_user(user_id: int, user: FarmerBase, db: db_dependency):
    update_user = db.query(models.Farmer).filter((models.Farmer.id) == user_id).first()
    if update_user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    
    update_user.password = user.password
    update_user.email = user.email
    update_user.username = user.username
    update_user.location = user.location
    update_user.farm_name = user.farm_name
    
    db.commit()
    return update_user

# to Delete Users by id
@farmer_router.delete('/{user_id}', status_code=status.HTTP_200_OK)
async def get_user(user_id: int, db: db_dependency):
    user = db.query(models.Farmer).filter(models.Farmer.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User Not Found')
    db.delete(user)
    db.commit()
    return "User Deleted Successfull"

