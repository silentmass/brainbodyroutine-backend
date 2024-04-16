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


@app.get("/api/tasks", response_model=list[schemas.Task])
def read_tasks(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)
):
    print("read_tasks")
    tasks = crud.get_tasks(db, skip=skip, limit=limit)
    return tasks


@app.post("/api/tasks", response_model=schemas.TaskCreate)
def create_task(
  task: schemas.TaskCreate,
  db: Session = Depends(get_db),
):
    print(task)
    return crud.create_task(db, task)


@app.post("/api/tasks/{id}/delete")
def delete_task(id: int, db: Session = Depends(get_db)):
    db_task = crud.get_task(db=db, id=id)
    if not db_task:
        raise HTTPException(status_code=400, detail="Task not found")
    return crud.delete_task(db=db, task=db_task)
