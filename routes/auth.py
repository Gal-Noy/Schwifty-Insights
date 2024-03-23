from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
import utils.auth as u_auth
import data.users as users

router = APIRouter()


@router.post('/register')
def register(user_in: users.User):
    """
    Register endpoint
    :param user_in: User data {username, password}
    :return: Message
    """
    hashed_password = u_auth.pwd_context.hash(user_in.password)
    user_in.password = hashed_password
    if not users.add_user(user_in):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"User {user_in.username} already exists")
    return {"message": f"User {user_in.username} created successfully"}


@router.post('/token')
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """
    Login endpoint
    :param form_data:
    :return: Access token
    """
    user = u_auth.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect username or password")

    access_token_expires = u_auth.timedelta(minutes=u_auth.TOKEN_EXPIRATION)
    access_token = u_auth.create_access_token(data={"sub": form_data.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
