from fastapi import APIRouter

from backend.api.src.routes.auth.controller import (
    authenticate_user,
)
from backend.api.src.routes.users.controller import (
    create_user,
    get_user_by_username,
    get_users,
)
from backend.api.src.routes.utils.db_dependency import get_db
from .schemas import User, UserNextAuth, UserCreate

from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session


router_users = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@router_users.post("", response_model=UserNextAuth)
def get_user_ep(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db),
):
    user = authenticate_user(form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user:
        return user


@router_users.get("", response_model=list[User])
def get_all_users_ep(db: Session = Depends(get_db)):
    users = get_users(db)
    return users


@router_users.post("/create")
def create_user_ep(
    user: UserCreate,
    db: Session = Depends(get_db),
):
    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    return create_user(db, user=user)
