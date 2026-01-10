from datetime import datetime

from app.utils.generators import get_current_datetime
from sqlalchemy import UUID, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.root_model import RootModel
from app.types.auth import TypeUUID


# Model to handle the user information
class User(RootModel):
    __tablename__ = "users"

    user_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, unique=True, nullable=False
    )
    first_name: Mapped[str] = mapped_column(String, nullable=False)
    last_name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    country: Mapped[str] = mapped_column(String, nullable=True)
    state: Mapped[str] = mapped_column(String, nullable=True)
    city: Mapped[str] = mapped_column(String, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=get_current_datetime
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=get_current_datetime,
        onupdate=get_current_datetime,
    )
