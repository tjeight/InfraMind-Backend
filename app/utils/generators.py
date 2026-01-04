from app.configs.settings import settings
from uuid6 import uuid7
from datetime import datetime, timezone


def get_async_database_url():
    """This is the utility function to generate the database url"""
    # get all the details
    POSTGRES_USER = settings.POSTGRES_USER
    POSTGRES_DB = settings.POSTGRES_DB
    POSTGRES_PASSWORD = settings.POSTGRES_PASSWORD
    POSTGRES_PORT = settings.POSTGRES_PORT
    POSTGRES_HOST = settings.POSTGRES_HOST

    return f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def get_sync_database_url():
    """This is the utility function to generate the async database url"""
    # get all the details
    POSTGRES_USER = settings.POSTGRES_USER
    POSTGRES_DB = settings.POSTGRES_DB
    POSTGRES_PASSWORD = settings.POSTGRES_PASSWORD
    POSTGRES_PORT = settings.POSTGRES_PORT
    POSTGRES_HOST = settings.POSTGRES_HOST

    return f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"


def get_uuid():
    """This is the utility function for getting the uuid"""
    return uuid7()


def get_current_datetime():
    """This is the utility function to generate or get the current datetime"""
    return datetime.now(timezone.utc)
