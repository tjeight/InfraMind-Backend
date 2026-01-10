from datetime import datetime

from sqlalchemy import UUID, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.root_model import RootModel
from app.types.auth import TypeUUID
from app.utils.generators import get_current_datetime, get_uuid


# Model to handle predefined country information
class Country(RootModel):
    __tablename__ = "countries"

    country_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid,
    )
    country_name: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
    )
    country_code: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
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

    states = relationship("State", back_populates="country")
