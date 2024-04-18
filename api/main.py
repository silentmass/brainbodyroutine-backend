from typing import Union

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/hello")
def read_root():
    return {"Hello": "World"}


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/api/taskcategories", response_model=schemas.TaskCategory)
def create_task_category(
    task_category: schemas.TaskCategoryCreate, db: Session = Depends(get_db)
):
    db_task_category = crud.get_task_category_by_title(
        db, task_category_title=task_category.title
    )
    if db_task_category:
        raise HTTPException(status_code=400,
                            detail="Task category already registered")

    return crud.create_task_category(db=db, task_category=task_category)


@app.post("/api/taskcategory/{id}/update", response_model=schemas.TaskCategory)
def update_task_category(
    id: int, task_category: schemas.TaskCategory, db: Session = Depends(get_db)
):
    db_task_category = crud.get_task_category_by_id(db=db, id=id)
    if not db_task_category:
        raise HTTPException(status_code=400, detail="Task category not found")
    return crud.update_task_category(
        db=db, db_task_category=db_task_category, task_category=task_category
    )


@app.post("/api/taskcategory/{id}", response_model=schemas.TaskCategory)
def get_task_category(id: int, db: Session = Depends(get_db)):
    db_task_category = crud.get_task_category_by_id(db=db, id=id)
    if not db_task_category:
        raise HTTPException(status_code=400, detail="Task category not found")
    return db_task_category


@app.post("/api/taskcategory/{id}/delete")
def delete_task_category(id: int, db: Session = Depends(get_db)):
    db_task_category = crud.get_task_category_by_id(db=db, id=id)
    if not db_task_category:
        raise HTTPException(status_code=400, detail="Task category not found")
    return crud.delete_task_category(db=db, task_category=db_task_category)


@app.get("/api/taskcategories", response_model=list[schemas.TaskCategory])
def read_task_categories(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    task_categories = crud.get_task_categories(db, skip=skip, limit=limit)
    return task_categories

# Task operations


@app.get("/api/tasks", response_model=list[schemas.Task])
def read_tasks(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.post("/api/tasks", response_model=schemas.TaskCreate)
def create_task(
  task: schemas.TaskCreate,
  db: Session = Depends(get_db),
):
    return crud.create_task(db, task)


@app.post("/api/tasks/{id}/delete")
def delete_task(id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task_by_id(db=db, id=id)
    if not db_task:
        raise HTTPException(status_code=400, detail="Task not found")
    return crud.delete_task(db=db, task=db_task)


@app.post("/api/tasks/{id}", response_model=schemas.Task)
def get_task(id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task_by_id(db=db, id=id)

    if not db_task:
        raise HTTPException("Task not found")

    return db_task


@app.post("/api/tasks/{id}/update", response_model=schemas.Task)
def update_task(
    id: int,
    task: schemas.Task,
    db: Session = Depends(get_db)
):
    db_task = crud.get_task_by_id(db=db, id=id)

    if not db_task:
        raise HTTPException("Task not found")

    if not task.tags:
        task.tags = db_task.tags

    if not task.description_lists:
        task.description_lists = db_task.description_lists

    return crud.update_task(
        db=db,
        db_task=db_task,
        task=task
    )


# Task description list operations
@app.get(
    "/api/taskdescriptionlists/{task_id}",
    response_model=list[schemas.TaskDescriptionList])
def get_description_lists(
    task_id: int,
    db: Session = Depends(get_db)
):
    db_task = crud.get_task_by_id(db, task_id)
    if not db_task:
        raise HTTPException(
            status_code=400,
            detail="Task description list task not found"
        )

    description_lists = (
        crud
        .get_description_lists(
            db=db,
            task_id=task_id
        )
    )

    return description_lists


@app.post(
    "/api/tasks/{id}/descriptionlists",
    response_model=schemas.TaskDescriptionListCreate)
def create_description_list(
    id: int,
    description_list: schemas.TaskDescriptionListCreate,
    db: Session = Depends(get_db),
):
    db_task = crud.get_task_by_id(db=db, id=id)

    if not db_task:
        raise HTTPException(
            status_code=400,
            detail="Task description list task not found"
        )

    title = description_list.title
    db_title = (
        crud
        .get_description_list_by_title(
            db=db, task_id=id, title=title
        ))

    if db_title is not None:
        raise HTTPException(
            status_code=400,
            detail="Task description list already registered"
        )

    return crud.create_description_list(
        db=db,
        description_list=description_list
    )


@app.post(
    "/api/descriptionlists/{id}/update",
    response_model=schemas.TaskDescriptionList
)
def update_description_list(
    id: int,
    descriptionList: schemas.TaskDescriptionList,
    db: Session = Depends(get_db)
):
    print(descriptionList)
    db_list = crud.get_description_list_by_id(db, id)

    if (descriptionList.descriptions is None
            or not descriptionList.descriptions):
        descriptionList.descriptions = []

    if not db_list:
        raise HTTPException(status_code=400,
                            detail="Description list is not registered")

    return crud.update_description_list(db, db_list, descriptionList)


@app.post(
    "/api/descriptionlists/{id}/delete"
)
def delete_description_list(
    id: int,
    db: Session = Depends(get_db)
):
    db_task_description_list = crud.get_description_list_by_id(
        db=db, id=id
    )

    if not db_task_description_list:
        raise HTTPException(
            status_code=400,
            detail=(
                "Task description list"
                + f" {id} not found"
            )
        )

    return crud.delete_description_list(
        db=db,
        task_description_list=db_task_description_list
    )


@app.get(
    "/api/descriptionlists/{id}",
    response_model=schemas.TaskDescriptionList
)
def get_description_list(
  id: int,
  db: Session = Depends(get_db)
):
    db_list = crud.get_description_list_by_id(db, id)

    if not db_list:
        raise HTTPException(
            status_code=400,
            detail=f"Description list {id} not registered"
        )

    return db_list


# List description operations


@app.get(
    "/api/descriptionlists/{id}/descriptions",
    response_model=list[schemas.TaskDescription]
)
def get_list_descriptions(
    id: int,
    db: Session = Depends(get_db)
):
    db_list = crud.get_description_list_by_id(
        db=db,
        id=id
    )

    if not db_list:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Description list {id} not registered")
        )

    return (
        crud
        .get_list_descriptions(
            db=db,
            description_list_id=id
        )
    )


@app.post(
    "/api/descriptionlists/{id}/descriptions",
    response_model=schemas.TaskDescription
)
def create_list_description(
    id: int,
    description: schemas.TaskDescriptionCreate,
    db: Session = Depends(get_db)
):
    db_list = crud.get_description_list_by_id(db, id)

    if not db_list:
        raise HTTPException(f"Description list {id} not registered")

    return (crud.create_list_description(db, description=description))


@app.post(
    "/api/descriptions/{id}/update",
    response_model=schemas.TaskDescriptionList
)
def update_list_description(
    description: schemas.TaskDescriptionList,
    db: Session = Depends(get_db)
):
    db_description = crud.get_list_description_by_id(db, description.id)

    if not description:
        raise HTTPException(
            status_code=400, detail="Description is not registered")

    return crud.update_list_description(db, db_description, description)


@app.post(
    "/api/descriptions/{description_id}/delete",
)
def delete_list_description(
    description_id: int,
    db: Session = Depends(get_db)
):
    db_description = crud.get_list_description_by_id(db, description_id)

    if not db_description:
        raise HTTPException("List description not registered")

    return crud.delete_list_description(db, db_description)
