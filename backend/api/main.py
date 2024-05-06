import os
from typing import Annotated, Union

from fastapi.responses import RedirectResponse
import uvicorn
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from .src.routes.auth import main as auth_main
from .src.routes.descriptions import main as descriptions_main
from .src.routes.users import main as users_main
from .src.routes.descriptionlists import main as descriptionlists_main
from .src.routes.taskcategories import main as taskcategories_main
from .src.routes.tasks import main as tasks_main

from .src.routes.auth.controller import get_current_active_user
from .src.routes.users.schemas import User

from .src.config.database import engine

from .models import Base


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

Base.metadata.create_all(bind=engine)

app = FastAPI()

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

app.include_router(auth_main.router_auth)
app.include_router(descriptionlists_main.router_lists)
app.include_router(descriptions_main.router_descriptions)
app.include_router(users_main.router_users)
app.include_router(taskcategories_main.router_categories)
app.include_router(tasks_main.router_tasks)


@app.get("/")
async def root():
    return {"message": "Hello from FastAPI!"}


@app.get("/api/hello")
def read_root():
    return {"Hello": "World"}


# Swagger expects the auth-URL to be /token, but in our case it is /auth/token
# So, we redirect /token -> /auth/token
@app.post("/token")
def forward_to_login():
    """
    # Redirect
    to token-generation (`/auth/token`). Used to make Auth in Swagger-UI work.
    """
    return RedirectResponse(url="/api/authorize/token")


# Test endpoints


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


@app.get("/api/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


if __name__ == "__main__":
    uvicorn.run(
        "backend.api.main:app",
        host=os.getenv("API_HOST"),
        port=os.getenv("API_PORT"),
        reload=True,
    )