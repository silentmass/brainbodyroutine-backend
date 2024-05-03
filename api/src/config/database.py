import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv(".env.development.local")

SQLALCHEMY_DATABASE_URL = os.getenv("POSTGRES_URL").replace("postgres:",
                                                            "postgresql:")

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
