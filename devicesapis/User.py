"""CRUD Function for user in sqlalchemy"""
import models
import schemas
from passlib.hash import bcrypt
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: str):
    return db.query(
                    models.User).filter(
                        models.User.Username == user_id).first()


def get_user_by_Username(db: Session, Username: str):
    return db.query(
                    models.User).filter(
                        models.User.Username == Username).first()


def get_priviledge_by_Username(db: Session, Username: str):
    admin_var = (
        db.query(models.User)
        .where((models.User.Username == Username) & (models.User.Admin == 1))
        .first()
    )
    access = False
    if admin_var is not None:
        access = True
    return access


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = bcrypt.hash(user.hashed_password)
    db_user = models.User(
                          Username=user.Username,
                          hashed_password=hashed_password,
                          Admin=user.Admin
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, Username: str):
    db_user = db.query(
                        models.User).filter(
                            models.User.Username == Username).first()
    db.delete(db_user)
    db.commit()
    return None
