from datetime import datetime

from sqlalchemy import UUID, DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.root_model import RootModel
from app.types.auth import TypeUUID
from app.utils.generators import get_current_datetime, get_uuid


# Model to handle predefined city information
class City(RootModel):
    __tablename__ = "cities"

    city_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        nullable=False,
        default=get_uuid,
    )
    city_name: Mapped[str] = mapped_column(
        String, nullable=False, unique=True, index=True
    )

    state_id: Mapped[TypeUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("states.state_id", ondelete="CASCADE"),
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

    state = relationship("State", back_populates="cities")
