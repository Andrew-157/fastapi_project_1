import re
from sqlmodel import SQLModel, Field
from pydantic import validator


class UserBase(SQLModel):
    username: str = Field(max_length=255, min_length=5,
                          unique=True, index=True)
    email: str = Field(unique=True, max_length=255,
                       index=True)

    @validator("email")
    def email_valid(cls, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, value):
            raise ValueError("Not valid email address")
        return value


class RecommendationBase(SQLModel):
    type_of_fiction: str = Field(max_length=255,
                                 min_length=4, unique=True)
    title: str = Field(max_length=255)
    short_description: str
    opinion: str

    user_id: int = Field(foreign_key="user.id")


class TagBase(SQLModel):
    name: str = Field(max_length=255)


class UserCreate(UserBase):
    password: str = Field(min_length=8)


class UserRead(UserBase):
    id: int


class UserUpdate(SQLModel):
    username: str | None = Field(default=None,
                                 max_length=255, min_length=5)
    email: str | None = Field(default=None,
                              max_length=255)

    @validator("email")
    def email_valid(cls, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, value):
            raise ValueError("Not valid email address")
        return value
