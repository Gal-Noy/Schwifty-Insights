import os

from fastapi import Header
from fastapi.security import OAuth2PasswordBearer

import data.users as users
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
SECRET_KEY = os.getenv('SECRET_KEY')
TOKEN_EXPIRATION = int(os.getenv('TOKEN_EXPIRATION'))
ALGORITHM = "HS256"


def verify_password(plain, hashed):
    """
    Verify a password
    :param plain: Plain password
    :param hashed: Hashed password
    :return: True if the password is verified, False otherwise
    """
    return pwd_context.verify(plain, hashed)


def authenticate_user(username, password):
    """
    Authenticate a user
    :param username:
    :param password:
    :return: True if the user is authenticated, False otherwise
    """
    user = users.get_user(username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta = None):
    """
    Create an access token
    :param data:
    :param expires_delta:
    :return: Access token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(authorization: str = Header(...)):
    """
    Verify a token
    :param authorization:
    :return: Token
    """
    try:
        token = authorization.split("Bearer ")[1]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return {"error": "Token has expired"}
    except jwt.JWTError:
        return {"error": "Invalid token"}



