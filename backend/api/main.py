from fastapi.responses import FileResponse, RedirectResponse
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from backend.api.src.routes.auth import main as auth_main
from backend.api.src.routes.descriptions import main as descriptions_main
from backend.api.src.routes.users import main as users_main
from backend.api.src.routes.descriptionlists import (
    main as descriptionlists_main,
)
from backend.api.src.routes.taskcategories import main as taskcategories_main
from backend.api.src.routes.tasks import main as tasks_main

from backend.api.src.config.database import engine

from backend.api.models import Base


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

favicon_path = "backend/static/favicon.ico"


@app.get("/favicon.ico", include_in_schema=False)
async def favicon():
    return FileResponse(favicon_path)


@app.get("/api")
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


if __name__ == "__main__":
    # uvicorn.run(app)
    uvicorn.run("backend.api.main:app", host="0.0.0.0", port=8000, reload=True)
