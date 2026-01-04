from sqlalchemy import UUID, String
from sqlalchemy.orm import Mapped, mapped_column
from app.models.root_model import RootModel
from app.types.auth import TypeUUID
from app.utils.generators import get_uuid


# Class to Handle the User
class Users(RootModel):
    __tablename__ = "users"
    user_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=get_uuid
    )

    user_email: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False, unique=True)
