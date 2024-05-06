from passlib.context import CryptContext
from sqlalchemy.orm import Session

from api import models

from . import schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_users(db: Session):
    db_users = db.query(models.BBR_User).all()
    return db_users


def get_user_by_username(db: Session, username: str):
    db_user = (
        db.query(models.BBR_User)
        .filter(models.BBR_User.username == username)
        .first()
    )
    return db_user


def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.BBR_User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        disabled=user.disabled,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
