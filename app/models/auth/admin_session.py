from datetime import datetime

from sqlalchemy import UUID, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.root_model import RootModel
from app.types.auth import TypeUUID
from app.utils.generators import get_current_datetime, get_uuid


# Class to handle the Admin Session
class AdminSession(RootModel):
    __tablename__ = "admin_sessions"

    admin_session_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=get_uuid
    )
    admin_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("admins.admin_id", ondelete="CASCADE"),
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
