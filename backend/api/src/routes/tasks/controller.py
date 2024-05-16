from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.api.src.routes.descriptionlists.controller import (
    create_description_list,
)
from backend.api.src.routes.descriptionlists.schemas import (
    TaskDescriptionListCreate,
)
from backend.api.src.routes.descriptions.controller import (
    create_list_description,
)
from backend.api.src.routes.descriptions.schemas import TaskDescriptionCreate
from backend.api.src.routes.users.schemas import User

from .schemas import Task, TaskBase
from backend.api import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Task operations


def get_task_by_id(db: Session, id: int):
    return db.query(models.BBR_Task).filter(models.BBR_Task.id == id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.BBR_Task)
        .order_by(models.BBR_Task.sort_order)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_null_user_tasks(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(models.BBR_Task)
        .filter(models.BBR_Task.user_id.is_(None))
        .order_by(models.BBR_Task.sort_order)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_user_tasks(db: Session, user: User, skip: int = 0, limit: int = 100):
    return (
        db.query(models.BBR_Task)
        .filter(models.BBR_Task.user_id == user.id)
        .order_by(models.BBR_Task.sort_order)
        .offset(skip)
        .limit(limit)
        .all()
    )


def create_user_task(db: Session, task: TaskBase, user: User):
    db_task = models.BBR_Task(**task.model_dump(), user_id=user.id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)

    sorted_task = Task(
        id=db_task.id,
        title=db_task.title,
        task_category_id=db_task.task_category_id,
        is_active=db_task.is_active,
        user_id=db_task.user_id,
        sort_order=db_task.id * 100,
        tags=db_task.tags,
        description_lists=db_task.description_lists,
    )

    return update_task(db, db_task=db_task, task=sorted_task)


def copy_task_for_user(db: Session, task: Task, user: User):
    db_new_task = create_user_task(
        db,
        TaskBase(
            title=task.title,
            task_category_id=task.task_category_id,
            is_active=task.is_active,
        ),
        user,
    )

    # Update tags
    update_task(
        db,
        db_new_task,
        Task(
            id=db_new_task.id,
            title=db_new_task.title,
            task_category_id=db_new_task.task_category_id,
            is_active=db_new_task.is_active,
            user_id=db_new_task.user_id,
            sort_order=db_new_task.id * 100,
            tags=task.tags,
            description_lists=db_new_task.description_lists,
        ),
    )

    # Create descriptions
    for description_list in task.description_lists:
        # Create new list
        db_list = TaskDescriptionListCreate(
            title=description_list.title, task_id=db_new_task.task_id
        )
        new_db_list = create_description_list(db, db_list)

        for description in description_list:
            # Create new description
            db_description = TaskDescriptionCreate(
                description=description.description,
                description_list_id=new_db_list.description_list_id,
            )
            create_list_description(db, db_description)

    return get_task_by_id(db, db_new_task.id)


def update_task(
    db: Session,
    db_task: Task,
    task: Task,
):
    db_task.title = task.title
    db_task.task_category_id = task.task_category_id
    db_task.is_active = task.is_active
    db_task.sort_order = task.sort_order
    db_task.tags = task.tags
    db_task.description_lists = task.description_lists
    db.commit()
    return db_task


def delete_task(db: Session, task: Task):
    db.delete(task)
    db.commit()
    return True
