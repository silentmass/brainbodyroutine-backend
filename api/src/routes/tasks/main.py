from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.src.routes.auth.controller import get_current_active_user
from api.src.routes.tasks.controller import (
    create_task,
    delete_task,
    get_task_by_id,
    get_tasks,
    update_task,
)
from api.src.routes.tasks.schemas import Task, TaskCreate
from api.src.routes.users.schemas import User
from api.src.routes.utils.db_dependency import get_db


router_tasks = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"],
)

# Task operations


@router_tasks.get("", response_model=list[Task])
def get_tasks_ep(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    tasks = get_tasks(db, skip=skip, limit=limit)
    return tasks


@router_tasks.post("/{id}", response_model=Task)
def get_task_by_id_ep(id: int, db: Session = Depends(get_db)):
    db_task = get_task_by_id(db=db, id=id)

    if not db_task:
        raise HTTPException("Task not found")

    return db_task


@router_tasks.post("", response_model=TaskCreate)
def create_task_ep(
    task: TaskCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return create_task(db, task)


@router_tasks.post("/{id}/delete")
def delete_task_ep(
    id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_task = get_task_by_id(db=db, id=id)
    if not db_task:
        raise HTTPException(status_code=400, detail="Task not found")
    return delete_task(db=db, task=db_task)


@router_tasks.post("/{id}/update", response_model=Task)
def update_task_ep(
    id: int,
    task: Task,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_task = get_task_by_id(db=db, id=id)

    if not db_task:
        raise HTTPException("Task not found")

    if not task.tags:
        task.tags = db_task.tags

    if not task.description_lists:
        task.description_lists = db_task.description_lists

    return update_task(db=db, db_task=db_task, task=task)
