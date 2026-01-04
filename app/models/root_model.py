from sqlalchemy.orm import DeclarativeBase


# Root Model to inherit by other models
class RootModel(DeclarativeBase):
    """This is the class to be inherited by other models"""
