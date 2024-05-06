from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import schemas

from backend.api import models

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# List description operations


def get_list_descriptions(db: Session, description_list_id: int):
    return (
        db.query(models.BBR_TaskDescription)
        .filter(
            (
                models.BBR_TaskDescription.description_list_id
                == description_list_id
            )
        )
        .all()
    )


def get_list_description_by_id(db: Session, id: int):
    return (
        db.query(models.BBR_TaskDescription)
        .filter(models.BBR_TaskDescription.id == id)
        .first()
    )


def create_list_description(
    db: Session, description: schemas.TaskDescriptionCreate
):
    db_description = models.BBR_TaskDescription(**description.model_dump())
    db.add(db_description)
    db.commit()
    db.refresh(db_description)
    return db_description


def update_list_description(
    db: Session,
    db_description: schemas.TaskDescription,
    description: schemas.TaskDescription,
):
    db_description.description = description.description
    db_description.description_list_id = description.description_list_id
    db.commit()
    return db_description


def delete_list_description(db: Session, description: schemas.TaskDescription):
    db.delete(description)
    db.commit()
    return True
