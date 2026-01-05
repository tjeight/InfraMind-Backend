from datetime import datetime

from sqlalchemy import UUID, DateTime, ForeignKey
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

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_current_datetime, nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_current_datetime,
        onupdate=get_current_datetime,
        nullable=False,
    )
