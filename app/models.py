from sqlmodel import SQLModel, Field
from .schemas import UserBase


class User(UserBase, table=True):
    int: int | None = Field(default=None, primary_key=True)
    hashed_password: str
