from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.api.src.routes.utils.db_dependency import get_db
from backend.api.src.routes.taskcategories.controller import (
    get_task_categories,
    get_task_category_by_id,
)
from backend.api.src.routes.taskcategories.schemas import (
    TaskCategory,
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
