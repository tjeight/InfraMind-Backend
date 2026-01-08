from app.utils.generators import get_current_datetime
from app.configs.settings import settings
import jwt
import bcrypt


def hash_password(password: str) -> str:
    """This is the utility function to generate the hash password"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """This is the utility function to verify the password"""
    return bcrypt.checkpw(
        plain_password.encode("utf-8"), hashed_password.encode("utf-8")
    )


def create_access_token(
    payload: dict,
) -> str:
    """This is the utility function to create the access token"""

    # get the data
    data = payload.copy()

    # update the data with the expiry
    expire = get_current_datetime() + settings.access_token_expire

    # add the expire
    data.update({"exp": expire})

    # sign the token
    token = jwt.encode(
        data,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token


def create_refresh_token(
    payload: dict,
) -> str:
    """This is the utility function to create the refresh token"""

    # get the data
    data = payload.copy()

    # update the data with the expiry
    expire = get_current_datetime() + settings.refresh_token_expire

    # add the expire
    data.update({"exp": expire})

    # sign the token
    token = jwt.encode(
        data,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM,
    )

    return token
