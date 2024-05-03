from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import schemas
from api import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Task operations


def get_task_by_id(db: Session, id: int):
    return db.query(models.Task).filter(models.Task.id == id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def update_task(
    db: Session,
    db_task: schemas.Task,
    task: schemas.Task,
):
    db_task.title = task.title
    db_task.task_category_id = task.task_category_id
    db_task.is_active = task.is_active
    db_task.tags = task.tags
    db_task.description_lists = task.description_lists
    db.commit()
    return db_task


def delete_task(db: Session, task: schemas.Task):
    db.delete(task)
    db.commit()
    return True
