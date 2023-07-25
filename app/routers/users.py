import re
from datetime import datetime, timedelta

from decouple import config
from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session
from ..schemas import UserRead, UserCreate
from ..models import User
from ..database import engine
from .users_crud import get_user_with_email, get_user_with_username

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 5


router = APIRouter(tags=["users"],
                   prefix="/auth")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_password_hash(password):
    return pwd_context.hash(password)


def get_session():
    with Session(engine) as session:
        yield session


@router.post("/register", response_model=UserRead)
async def register(*, session: Session = Depends(get_session), user: UserCreate):
    hashed_password = get_password_hash(password=user.password)
    if get_user_with_username(session, user.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Not unique username")
    if get_user_with_email(session, user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Not unique email")
    db_user = User(username=user.username,
                   email=user.email,
                   hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user
