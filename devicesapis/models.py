""" Base model definition for authentication."""
from database import Base
from passlib.hash import bcrypt
from sqlalchemy import Boolean, Column, Integer, String


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    Username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    Admin = Column(Boolean, default=True)

    class Config:
        orm_mode = True

    def verify_password(self, password):
        return bcrypt.verify(password, self.hashed_password)
