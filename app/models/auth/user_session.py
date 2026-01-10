from datetime import datetime

from sqlalchemy import UUID, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.root_model import RootModel
from app.types.auth import TypeUUID
from app.utils.generators import get_current_datetime, get_uuid


# Model to handle the user session information
class UserSession(RootModel):
    __tablename__ = "user_sessions"

    user_session_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=get_uuid
    )
    user_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        nullable=False,
    )
    ip_address: Mapped[str | None] = mapped_column(
        String(45),  # IPv6-safe
        nullable=True,
    )
    refresh_token: Mapped[str] = mapped_column(String, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_current_datetime, nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_current_datetime,
        onupdate=get_current_datetime,
        nullable=False,
    )
