from pydantic import BaseModel

users_db = {}


class User(BaseModel):
    username: str
    password: str


def add_user(user: User):
    """
    Add a user to the database
    :param user:
    :return: True if the user was added, False otherwise
    """
    if user.username in users_db:
        return False
    users_db[user.username] = user.password
    return True


def get_user(username: str):
    """
    Get a user from the database
    :param username:
    :return: User if the user exists, None otherwise
    """
    if username not in users_db:
        return None
    return User(username=username, password=users_db[username])
