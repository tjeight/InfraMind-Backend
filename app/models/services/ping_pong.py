from datetime import datetime
from sqlalchemy import Integer, Boolean, DateTime, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.root_model import RootModel
from app.types.auth import TypeUUID
from app.utils.generators import get_uuid, get_current_datetime


class ServicePingLog(RootModel):
    __tablename__ = "service_ping_logs"

    ping_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=get_uuid
    )

    service_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("services.service_id", ondelete="CASCADE"),
        nullable=False,
    )

    status_code: Mapped[int | None] = mapped_column(Integer, nullable=True)
    response_time_ms: Mapped[int | None] = mapped_column(Integer, nullable=True)

    is_success: Mapped[bool] = mapped_column(Boolean, nullable=False)

    checked_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_current_datetime, nullable=False
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
