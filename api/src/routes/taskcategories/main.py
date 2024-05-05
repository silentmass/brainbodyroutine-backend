from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.src.routes.auth.controller import get_current_active_user
from api.src.routes.users.schemas import User
from api.src.routes.utils.db_dependency import get_db
from api.src.routes.taskcategories.controller import (
    create_task_category,
    delete_task_category,
    get_task_categories,
    get_task_category_by_id,
    get_task_category_by_title,
    update_task_category,
)
from api.src.routes.taskcategories.schemas import (
    TaskCategory,
    TaskCategoryCreate,
)

router_categories = APIRouter(
    prefix="/api/taskcategories",
    tags=["Taskcategories"],
)


@router_categories.get("", response_model=list[TaskCategory])
def read_task_categories_ep(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    task_categories = get_task_categories(db, skip=skip, limit=limit)
    return task_categories


@router_categories.post("/{id}", response_model=TaskCategory)
def get_task_category_ep(id: int, db: Session = Depends(get_db)):
    db_task_category = get_task_category_by_id(db=db, id=id)
    if not db_task_category:
        raise HTTPException(status_code=400, detail="Task category not found")
    return db_task_category


@router_categories.post("", response_model=TaskCategoryCreate)
def create_task_category_ep(
    task_category: TaskCategoryCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_task_category = get_task_category_by_title(
        db, task_category_title=task_category.title
    )
    if db_task_category:
        raise HTTPException(
            status_code=400, detail="Task category already registered"
        )

    return create_task_category(db=db, task_category=task_category)


@router_categories.post("/{id}/update", response_model=TaskCategory)
def update_task_category_ep(
    id: int,
    task_category: TaskCategory,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_task_category = get_task_category_by_id(db=db, id=id)
    if not db_task_category:
        raise HTTPException(status_code=400, detail="Task category not found")
    return update_task_category(
        db=db, db_task_category=db_task_category, task_category=task_category
    )


@router_categories.post("/{id}/delete")
def delete_task_category_ep(
    id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_task_category = get_task_category_by_id(db=db, id=id)
    if not db_task_category:
        raise HTTPException(status_code=400, detail="Task category not found")
    return delete_task_category(db=db, task_category=db_task_category)
