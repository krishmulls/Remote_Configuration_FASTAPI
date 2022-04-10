"""Dependencies for Authentication and session user fetching function."""
import fastapi
import jwt
import models
import schemas
from database import SessionLocal
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

JWT_SECRET = "R3kFO9wgQADwVJ8pf6VXA"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(
    db: Session = fastapi.Depends(get_db),
    token: str = fastapi.Depends(oauth2_scheme)
):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        user = (
            db.query(models.User)
            .filter(models.User.Username == payload.get("Username"))
            .first()
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
        )
    return schemas.User.from_orm(user)
