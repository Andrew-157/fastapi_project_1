from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(unique=True, max_length=255)
    email: str = Field(unique=True, max_length=255)
    hashed_password: str
