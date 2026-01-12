from datetime import datetime
from sqlalchemy import String, Integer, DateTime, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.root_model import RootModel
from app.types.auth import TypeUUID
from app.utils.generators import get_uuid, get_current_datetime


class ServiceHealthCheck(RootModel):
    __tablename__ = "service_health_checks"

    health_check_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=get_uuid
    )

    service_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("services.service_id", ondelete="CASCADE"),
        nullable=False,
    )

    path: Mapped[str] = mapped_column(String, default="/health", nullable=False)
    method: Mapped[str] = mapped_column(String, default="GET", nullable=False)
    expected_status: Mapped[int] = mapped_column(Integer, default=200, nullable=False)

    timeout_ms: Mapped[int] = mapped_column(Integer, default=3000, nullable=False)
    interval_seconds: Mapped[int] = mapped_column(Integer, default=60, nullable=False)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=get_current_datetime, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=get_current_datetime,
        onupdate=get_current_datetime,
        nullable=False,
    )
