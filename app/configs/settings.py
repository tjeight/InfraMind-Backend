from pydantic_settings import BaseSettings, SettingsConfigDict


# Settings class for getting the environment variables
class Settings(BaseSettings):
    POSTGRES_DB: str = ""
    POSTGRES_USER: str = ""
    POSTGRES_PASSWORD: str = ""
    POSTGRES_PORT: int = 0
    POSTGRES_HOST: str = ""
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


# create an object of the settings class
settings = Settings()
