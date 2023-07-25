from sqlmodel import SQLModel, Field


class UserBase(SQLModel):
    username: str = Field(unique=True, max_length=255)
    email: str = Field(unique=True, max_length=255)


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
