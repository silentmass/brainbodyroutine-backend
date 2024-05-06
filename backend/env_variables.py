from dotenv import load_dotenv
import os

load_dotenv(".env")
SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_URL").replace(
    "postgres:", "postgresql:"
)
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
