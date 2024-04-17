from sqlalchemy.orm import Session

from . import models, schemas

# Task category operations


def get_task_category_by_title(db: Session, task_category_title: str):
    return (
        db.query(models.TaskCategory)
        .filter(models.TaskCategory.title == task_category_title)
        .first()
    )


def get_task_category_by_id(db: Session, id: int):
    return (
        db
        .query(models.TaskCategory)
        .filter(models.TaskCategory.id == id)
        .first()
    )


def get_task_categories(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.TaskCategory).offset(skip).limit(limit).all()


def create_task_category(
    db: Session,
    task_category: schemas.TaskCategoryCreate
):
    db_task_category = models.TaskCategory(**task_category.model_dump())
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

# Task operations


def get_task_by_id(db: Session, id: int):
    return db.query(models.Task).filter(models.Task.id == id).first()


def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()


def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        **task.model_dump()
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task: schemas.Task):
    db.delete(task)
    db.commit()
    return True


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


# Description list operations


def get_task_description_lists(
    db: Session,
    task_id: int
):
    return (
        db
        .query(models.TaskDescriptionList)
        .filter(models.TaskDescriptionList.task_id == task_id)
        .all()
    )


def create_task_description_list(
    db: Session,
    description_list: schemas.TaskDescriptionListCreate
):
    db_description_list = models.TaskDescriptionList(
        **description_list.model_dump()
    )
    print(db_description_list)
    db.add(db_description_list)
    db.commit()
    db.refresh(db_description_list)
    return db_description_list


def get_task_description_list_by_id(
    db: Session,
    id: int
):
    return (
        db
        .query(models.TaskDescriptionList)
        .filter(models.TaskDescriptionList.id == id)
        .first()
    )


def get_task_description_list_by_title(
    db: Session,
    task_id: int,
    title: str
):
    return (
        db
        .query(models.TaskDescriptionList)
        .filter(models.TaskDescriptionList.task_id == task_id,
                models.TaskDescriptionList.title == title)
        .first()
    )


def delete_task_description_list(
    db: Session,
    task_description_list: schemas.TaskDescriptionList
):
    db.delete(task_description_list)
    db.commit()
    return True


# Description operations


def get_task_description_list_descriptions(
    db: Session,
    description_list_id: int
):
    return (
        db
        .query(models.TaskDescription)
        .filter(
            (models.TaskDescription.description_list_id
             == description_list_id)
        )
        .all()
    )


def get_list_description_by_id(
    db: Session,
    id: int
):
    return (
        db
        .query(models.TaskDescription)
        .filter(models.TaskDescription.id == id)
        .first()
    )


def create_task_list_description(
    db: Session,
    description: schemas.TaskDescriptionCreate
):
    db_description = models.TaskDescription(
        **description.model_dump()
    )
    db.add(db_description)
    db.commit()
    db.refresh(db_description)
    return db_description


def delete_list_description(
  db: Session,
  description: schemas.TaskDescription
):
    db.delete(description)
    db.commit()
    return True
