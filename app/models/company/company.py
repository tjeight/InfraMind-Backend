from datetime import datetime
from sqlalchemy import UUID, Boolean, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.root_model import RootModel
from app.types.auth import TypeUUID
from app.utils.generators import get_current_datetime, get_uuid


class Company(RootModel):
    __tablename__ = "companies"

    company_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True), unique=True, nullable=False, default=get_uuid
    )
    company_name: Mapped[str] = mapped_column(String, nullable=False)
    company_slug: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    company_website: Mapped[str] = mapped_column(String, nullable=True)
    user_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=get_current_datetime
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=get_current_datetime,
        onupdate=get_current_datetime,
    )
