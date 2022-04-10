"""Defining schemas for difference api use-cases."""
from pydantic import BaseModel


class UserBase(BaseModel):
    Username: str


class UserCreate(UserBase):
    hashed_password: str
    Admin: bool


class User(UserBase):
    id: int

    class Config:
        orm_mode = True


class Users(UserBase):
    id: int
    hashed_password: str
    Admin: bool

    class Config:
        orm_mode = True
