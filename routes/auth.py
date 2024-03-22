from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import utils.auth as u_auth
import data.users as users

router = APIRouter()


@router.post('/token')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Login endpoint
    :param form_data:
    :return:
    """
    user = u_auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    access_token_expires = u_auth.timedelta(minutes=u_auth.TOKEN_EXPIRATION)
    access_token = u_auth.create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post('/register')
def register(username: str, password: str):
    """
    Register endpoint
    :param username:
    :param password:
    :return:
    """
    hashed_password = u_auth.pwd_context.hash(password)
    user = users.User(username=username, password=hashed_password)
    if not users.add_user(user):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="User already exists")
    return {"message": "User created successfully"}