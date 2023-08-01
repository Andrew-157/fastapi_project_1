import re
from sqlmodel import SQLModel, Field
from pydantic import validator


class UserBase(SQLModel):
    name: str = Field(max_length=255, min_length=5,
                      unique=True, index=True)
    email: str = Field(unique=True, max_length=255,
                       index=True)

    def email_valid(cls, value):
        regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
        if not re.fullmatch(regex, value):
            raise ValueError("Not valid email address")
        return value
