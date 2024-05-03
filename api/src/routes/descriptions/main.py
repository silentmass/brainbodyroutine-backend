from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from api.src.routes.descriptionlists.controller import (
    get_description_list_by_id,
)
from api.src.routes.descriptions.controller import (
    create_list_description,
    delete_list_description,
    get_list_description_by_id,
    get_list_descriptions,
    update_list_description,
)
from api.src.routes.descriptions.schemas import (
    TaskDescription,
    TaskDescriptionCreate,
)
from api.src.routes.utils.db_dependency import get_db
from api.src.routes.descriptionlists.main import router_lists

router_descriptions = APIRouter(
    prefix="/api/descriptions",
    tags=["Descriptions"],
)

# List description operations


@router_lists.get(
    "/{id}/descriptions",
    response_model=list[TaskDescription],
)
def get_list_descriptions_ep(id: int, db: Session = Depends(get_db)):
    db_list = get_description_list_by_id(db=db, id=id)

    if not db_list:
        raise HTTPException(
            status_code=400, detail=(f"Description list {id} not registered")
        )

    return get_list_descriptions(db=db, description_list_id=id)


@router_lists.post(
    "/{id}/descriptions",
    response_model=TaskDescription,
)
def create_list_description_ep(
    id: int,
    description: TaskDescriptionCreate,
    db: Session = Depends(get_db),
):
    db_list = get_description_list_by_id(db, id)

    if not db_list:
        raise HTTPException(f"Description list {id} not registered")

    return create_list_description(db, description=description)


@router_descriptions.post("/{id}/update", response_model=TaskDescription)
def update_list_description_ep(
    description: TaskDescription, db: Session = Depends(get_db)
):
    db_description = get_list_description_by_id(db, description.id)

    if not description:
        raise HTTPException(
            status_code=400, detail="Description is not registered"
        )

    return update_list_description(db, db_description, description)


@router_descriptions.post(
    "/{description_id}/delete",
)
def delete_list_description_ep(
    description_id: int, db: Session = Depends(get_db)
):
    db_description = get_list_description_by_id(db, description_id)

    if not db_description:
        raise HTTPException("List description not registered")

    return delete_list_description(db, db_description)
