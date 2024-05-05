from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from api.src.routes.auth.controller import get_current_active_user
from api.src.routes.descriptionlists.controller import (
    create_description_list,
    delete_description_list,
    get_description_list_by_id,
    get_task_description_list_by_title,
    get_description_lists_by_task_id,
    update_description_list,
)
from api.src.routes.descriptionlists.schemas import (
    TaskDescriptionList,
    TaskDescriptionListCreate,
)
from api.src.routes.tasks.controller import get_task_by_id
from api.src.routes.users.schemas import User
from api.src.routes.utils.db_dependency import get_db
from api.src.routes.tasks.main import router_tasks

router_lists = APIRouter(
    prefix="/api/descriptionlists",
    tags=["Descriptionslists"],
)

# Task description list operations


@router_tasks.get(
    "/{id}/descriptionlists",
    response_model=list[TaskDescriptionList],
)
def get_description_lists_by_task_id_ep(
    id: int, db: Session = Depends(get_db)
):
    db_task = get_task_by_id(db, id)
    if not db_task:
        raise HTTPException(
            status_code=400, detail="Task description list task not found"
        )

    description_lists = get_description_lists_by_task_id(db=db, task_id=id)

    return description_lists


@router_lists.get("/{id}", response_model=TaskDescriptionList)
def get_description_list_by_id_ep(id: int, db: Session = Depends(get_db)):
    db_list = get_description_list_by_id(db, id)

    if not db_list:
        raise HTTPException(
            status_code=400, detail=f"Description list {id} not registered"
        )

    return db_list


@router_tasks.post(
    "/{id}/descriptionlists",
    response_model=TaskDescriptionListCreate,
)
def create_description_list_ep(
    id: int,
    description_list: TaskDescriptionListCreate,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_task = get_task_by_id(db=db, id=id)

    if not db_task:
        raise HTTPException(
            status_code=400, detail="Task description list task not found"
        )

    title = description_list.title
    db_title = get_task_description_list_by_title(
        db=db, task_id=id, title=title
    )

    if db_title is not None:
        raise HTTPException(
            status_code=400, detail="Task description list already registered"
        )

    return create_description_list(db=db, description_list=description_list)


@router_lists.post(
    "/{id}/update",
    response_model=TaskDescriptionList,
)
def update_description_list_ep(
    id: int,
    descriptionList: TaskDescriptionList,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_list = get_description_list_by_id(db, id)

    if not db_list:
        raise HTTPException(
            status_code=400, detail="Description list is not registered"
        )

    if descriptionList.descriptions is None:
        descriptionList.descriptions = db_list.descriptions

    return update_description_list(db, db_list, descriptionList)


@router_lists.post("/{id}/delete")
def delete_description_list_ep(
    id: int,
    current_user: Annotated[User, Depends(get_current_active_user)],
    db: Session = Depends(get_db),
):
    db_task_description_list = get_description_list_by_id(db=db, id=id)

    if not db_task_description_list:
        raise HTTPException(
            status_code=400,
            detail=("Task description list" + f" {id} not found"),
        )

    return delete_description_list(
        db=db, task_description_list=db_task_description_list
    )
