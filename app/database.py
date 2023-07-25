from sqlmodel import create_engine, SQLModel
from decouple import config

from . import models

DATABASE_URL = config("DATABASE_URL")

connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL,
                       connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
