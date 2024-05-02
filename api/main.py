import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional, Union

import uvicorn
from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine
from .schemas import Token, TokenData, User

load_dotenv(".env")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_passwords(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


@app.post("/api/user", response_model=schemas.UserNextAuth)
def get_user(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
):
    user = authenticate_user(
        form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if user:
        return user


@app.get("/users", response_model=list[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


@app.post("/api/user/create")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    print("Create user")
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    return crud.create_user(db, user=user)


def authenticate_user(
    username: str, password: str, db: Session = Depends(get_db)
):
    user = crud.get_user(username=username, db=db)
    if not user:
        return False
    if not verify_passwords(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expired_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expired_delta:
        expire = datetime.now(timezone.utc) + expired_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = crud.get_user(username=token_data.username, db=db)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


# @app.post("/token")
@app.post("/api/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(get_db)
) -> Token:
    # Change db here and in arguments !!!
    user = authenticate_user(
        form_data.username, form_data.password, db=db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expired_delta=access_token_expires
    )
    return Token(
        access_token=access_token,
        token_type="bearer",
    )


@app.get("/api/users/me", response_model=User)
async def read_user_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/api/users/me/items")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


origins = [
    "http://127.0.0.1:3000",
    "127.0.0.1:3000",
    "https://brainbodyroutine2-gwz0l946r-juha-leukkunens-projects.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}


@app.get("/api/hello")
def read_root():
    return {"Hello": "World"}


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/api/taskcategories", response_model=schemas.TaskCategoryCreate)
def create_task_category(
    task_category: schemas.TaskCategoryCreate, db: Session = Depends(get_db)
):
    print("create_task_category", task_category)
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
  current_user: Annotated[User, Depends(get_current_active_user)],
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
    db_list = crud.get_description_list_by_id(db, id)

    if not db_list:
        raise HTTPException(status_code=400,
                            detail="Description list is not registered")

    if descriptionList.descriptions is None:
        descriptionList.descriptions = db_list.descriptions

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
    response_model=schemas.TaskDescription
)
def update_list_description(
    description: schemas.TaskDescription,
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


if __name__ == "__main__":
    uvicorn.run("api.main:app",
                host=os.getenv("API_HOST"),
                port=os.getenv("API_PORT"),
                reload=True)
