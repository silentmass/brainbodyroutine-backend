from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import schemas

from api import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_task_category_by_title(db: Session, task_category_title: str):
    return (
        db.query(models.BBR_TaskCategory)
        .filter(models.BBR_TaskCategory.title == task_category_title)
        .first()
    )


def get_task_category_by_id(db: Session, id: int):
    return (
        db.query(models.BBR_TaskCategory)
        .filter(models.BBR_TaskCategory.id == id)
        .first()
    )


def get_task_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.BBR_TaskCategory).offset(skip).limit(limit).all()


def create_task_category(
    db: Session, task_category: schemas.TaskCategoryCreate
):
    db_task_category = models.BBR_TaskCategory(**task_category.model_dump())
    db.add(db_task_category)
    db.commit()
    db.refresh(db_task_category)
    return db_task_category


def update_task_category(
    db: Session,
    db_task_category: schemas.TaskCategory,
    task_category: schemas.TaskCategory,
):
    db_task_category.title = task_category.title
    db_task_category.description = task_category.description
    db.commit()
    return db_task_category


def delete_task_category(db: Session, task_category: schemas.TaskCategory):
    db.delete(task_category)
    db.commit()
    return True
