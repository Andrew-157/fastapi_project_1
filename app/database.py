from sqlmodel import create_engine, SQLModel
from decouple import config

from . import models

DATABASE_URL = config("DATABASE_URL")

engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
