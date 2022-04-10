"""Sever main module for all the router api & user session & authentication."""
from typing import List

import fastapi
import jwt
import models
import schemas
import User
import uvicorn
from database import engine
from dependencies import JWT_SECRET, get_current_user, get_db
from devices.pm100d import router
from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from sqlalchemy.orm import Session

models.Base.metadata.create_all(bind=engine)

api = FastAPI()
templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def authenticate_user(db: Session, username: str, password: str):
    user = User.get_user_by_Username(db, Username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user


@api.post("/token")
async def generate_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = await authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication check Pass and user for auth",
        )
    user_obj = jsonable_encoder(user)
    token = jwt.encode(user_obj, JWT_SECRET)
    return {"access_token": token, "token_type": "bearer"}


@api.get("/")
async def devicesapi(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "Status": "Okay"}
    )


@api.get("/users/me", response_model=schemas.User)
async def get_user(user: schemas.UserBase = fastapi.Depends(get_current_user)):
    return user


@api.post("/admin/{Admin_id}")
def create_user(
    Admin_id: str,
    users: schemas.UserCreate,
    db: Session = Depends(get_db),
    user: schemas.UserBase = fastapi.Depends(get_current_user),
):
    db_user = User.get_user_by_Username(db, Username=users.Username)
    priviledge_check = User.get_priviledge_by_Username(db, Username=Admin_id)
    if db_user:
        raise HTTPException(status_code=400,
                            detail="Username already registered")
    if priviledge_check is True:
        User.create_user(db=db, user=users)
    return {"Priviliedge": priviledge_check}


@api.delete("/deleteuser/{Username}")
def delete_user(
    Username: str,
    users: schemas.Users,
    form_data: OAuth2PasswordBearer = Depends(),
    db: Session = Depends(get_db),
    user: schemas.UserBase = fastapi.Depends(get_current_user),
):
    db_user = User.get_user_by_Username(db, Username=Username)
    priviledge_check = User.get_priviledge_by_Username(
                                                    db,
                                                    Username=users.Username)
    if db_user:
        if priviledge_check is True:
            User.delete_user(db=db, Username=Username)
    else:
        raise HTTPException(
            status_code=400,
            detail="No permission to delete or No user found to delete",
        )
    return {"Priviliedge": priviledge_check}


@api.get("/users/", response_model=List[schemas.Users])
def read_users(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    user: schemas.UserBase = fastapi.Depends(get_current_user),
):
    users = User.get_users(db, skip=skip, limit=limit)
    return users


@api.get("/users/{user_id}", response_model=schemas.Users)
def read_user(
    user_id: str,
    db: Session = Depends(get_db),
    user: schemas.UserBase = fastapi.Depends(get_current_user),
):
    db_user = User.get_user_by_Username(db, Username=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


api.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "main:api",
        host="192.168.0.197",
        port=8000, reload=True,
        access_log=False
    )
