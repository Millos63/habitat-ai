from __future__ import annotations

import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class PropertyType(str, enum.Enum):
    """Available property types."""

    HOUSE = "house"
    APARTMENT = "apartment"
    LAND = "land"
    COMMERCIAL = "commercial"
    OFFICE = "office"


class PropertyStatus(str, enum.Enum):
    """Available property lifecycle statuses."""

    ACTIVE = "active"
    PAUSED = "paused"
    SOLD = "sold"
    RENTED = "rented"


class PropertyOperation(str, enum.Enum):
    """Available property operations."""

    SALE = "sale"
    RENT = "rent"


class Property(Base):
    """Real estate property listing model."""

    __tablename__ = "properties"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    agent_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    title: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    price: Mapped[Decimal] = mapped_column(Numeric(15, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False, default="MXN", server_default="MXN")

    type: Mapped[PropertyType | None] = mapped_column(
        Enum(
            PropertyType,
            name="property_type",
            values_callable=lambda enum_values: [member.value for member in enum_values],
        ),
        nullable=True,
        index=True,
    )
    status: Mapped[PropertyStatus] = mapped_column(
        Enum(
            PropertyStatus,
            name="property_status",
            values_callable=lambda enum_values: [member.value for member in enum_values],
        ),
        nullable=False,
        default=PropertyStatus.ACTIVE,
        server_default=PropertyStatus.ACTIVE.value,
        index=True,
    )
    operation: Mapped[PropertyOperation | None] = mapped_column(
        Enum(
            PropertyOperation,
            name="property_operation",
            values_callable=lambda enum_values: [member.value for member in enum_values],
        ),
        nullable=True,
        index=True,
    )

    address: Mapped[str] = mapped_column(Text, nullable=False)
    city: Mapped[str | None] = mapped_column(String(255), nullable=True, index=True)
    state: Mapped[str | None] = mapped_column(String(255), nullable=True)

    bedrooms: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    bathrooms: Mapped[int] = mapped_column(Integer, nullable=False, default=0, server_default="0")
    area_m2: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    images: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True)
    is_featured: Mapped[bool] = mapped_column(nullable=False, default=False, server_default="false", index=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
