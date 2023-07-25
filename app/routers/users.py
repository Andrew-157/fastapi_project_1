import re
from datetime import datetime, timedelta
from typing import Annotated

from decouple import config
from fastapi import Depends, APIRouter, HTTPException, status, Body
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlmodel import Session
from ..schemas import UserRead, UserCreate, UserUpdate
from ..models import User
from ..database import engine
from .users_crud import get_user_with_email, get_user_with_username

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 5


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


router = APIRouter(tags=["users"],
                   prefix="/auth")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_session():
    with Session(engine) as session:
        yield session


def authenticate_user(*,
                      session: Session,
                      username: str, password: str):
    user = get_user_with_username(session=session, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token: Annotated[str, Depends(oauth2_scheme)],
                     session: Session = Depends(get_session)):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credential_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credential_exception
    user = get_user_with_username(
        session=session, username=token_data.username)
    if user is None:
        raise credential_exception
    return user


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


@router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        session: Session = Depends(get_session)):
    user = authenticate_user(session=session,
                             username=form_data.username,
                             password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_HOURS)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me", response_model=UserRead)
async def read_users_me(
        current_user: Annotated[User, Depends(get_current_user)]
):
    return current_user


@router.put("/users/me/update", response_model=UserRead)
async def update_credentials(
        user_credentials: Annotated[UserUpdate, Body()],
        current_user: Annotated[User, Depends(get_current_user)],
        session: Session = Depends(get_session)):
    new_username = user_credentials.username
    new_email = user_credentials.email
    if get_user_with_username(session=session, username=new_username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Not unique username")
    if get_user_with_email(session=session, email=new_email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Not unique email")
    current_user.username = new_username
    current_user.email = new_email
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user
