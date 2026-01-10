from datetime import datetime

from sqlalchemy import UUID, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.root_model import RootModel
from app.types.auth import TypeUUID
from app.utils.generators import get_current_datetime, get_uuid


# Model to handle predefined state information
class State(RootModel):
    __tablename__ = "states"

    state_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid,
    )
    state_name: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
    )

    country_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("countries.country_id"),
        nullable=False,
        index=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=get_current_datetime
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=get_current_datetime,
        onupdate=get_current_datetime,
    )

    country = relationship("Country", back_populates="states")
