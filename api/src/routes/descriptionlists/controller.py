from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import schemas
from api import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Description list operations


def get_description_lists_by_task_id(db: Session, task_id: int):
    return (
        db.query(models.TaskDescriptionList)
        .filter(models.TaskDescriptionList.task_id == task_id)
        .all()
    )


def create_description_list(
    db: Session, description_list: schemas.TaskDescriptionListCreate
):
    db_description_list = models.TaskDescriptionList(
        **description_list.model_dump()
    )
    print(db_description_list)
    db.add(db_description_list)
    db.commit()
    db.refresh(db_description_list)
    return db_description_list


def get_description_list_by_id(db: Session, id: int):
    return (
        db.query(models.TaskDescriptionList)
        .filter(models.TaskDescriptionList.id == id)
        .first()
    )


def get_task_description_list_by_title(db: Session, task_id: int, title: str):
    return (
        db.query(models.TaskDescriptionList)
        .filter(
            models.TaskDescriptionList.task_id == task_id,
            models.TaskDescriptionList.title == title,
        )
        .first()
    )


def update_description_list(
    db: Session,
    db_list: schemas.TaskDescriptionList,
    new_list: schemas.TaskDescriptionList,
):
    db_list.title = new_list.title
    # db_list.descriptions = []
    # for description in new_list.descriptions:
    #     print(description)
    #     db_list.descriptions.append(description)
    db.commit()
    return db_list


def delete_description_list(
    db: Session, task_description_list: schemas.TaskDescriptionList
):
    db.delete(task_description_list)
    db.commit()
    return True
