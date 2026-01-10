from datetime import datetime

from app.utils.generators import get_current_datetime
from sqlalchemy import UUID, DateTime, ForeignKey, String
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
    country_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("countries.country_id"), nullable=True
    )
    state_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("states.state_id"), nullable=True
    )
    city_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("cities.city_id"), nullable=True
    )
    is_active: Mapped[bool] = mapped_column(nullable=False, default=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=get_current_datetime
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=get_current_datetime,
        onupdate=get_current_datetime,
    )
