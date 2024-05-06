from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.src.routes.auth.controller import get_current_active_user
from api.src.routes.tasks.controller import (
    copy_task_for_user,
    create_user_task,
    delete_task,
    get_task_by_id,
    get_tasks,
    get_user_tasks,
    update_task,
)
from api.src.routes.tasks.schemas import Task, TaskBase, TaskCreate
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


@router_tasks.post("", response_model=TaskCreate)
def create_task_ep(
    task: TaskBase,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return create_user_task(db, task, current_user)


@router_tasks.post("/user-tasks/copy", response_model=Task)
def copy_task_for_user_ep(
    task: Task,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    return copy_task_for_user(db, task, current_user)


@router_tasks.get("/user-tasks", response_model=list[Task])
def get_user_tasks_ep(
    current_user: Annotated[User, Depends(get_current_active_user)],
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return get_user_tasks(db, current_user, skip=skip, limit=limit)


@router_tasks.post("/user-tasks/{id}/delete")
def delete_user_task_ep(
    id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_task = get_task_by_id(db=db, id=id)
    if not db_task or db_task.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="User task not found")
    return delete_task(db=db, task=db_task)


@router_tasks.post("/{id}", response_model=Task)
def get_task_by_id_ep(id: int, db: Session = Depends(get_db)):
    db_task = get_task_by_id(db=db, id=id)

    if not db_task:
        raise HTTPException("Task not found")

    return db_task


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
