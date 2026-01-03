from app.configs.settings import settings


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
