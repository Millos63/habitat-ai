from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.models.property import PropertyOperation, PropertyStatus, PropertyType


class PropertyCreate(BaseModel):
    """Payload for creating or fully updating a property listing."""

    title: str = Field(min_length=3, max_length=500)
    description: str | None = None
    price: Decimal = Field(gt=0)
    currency: str = Field(default="MXN", min_length=3, max_length=3)
    type: PropertyType | None = None
    operation: PropertyOperation | None = None
    address: str = Field(min_length=5)
    city: str | None = Field(default=None, max_length=255)
    state: str | None = Field(default=None, max_length=255)
    bedrooms: int = Field(default=0, ge=0)
    bathrooms: int = Field(default=0, ge=0)
    area_m2: Decimal | None = Field(default=None, ge=0)
    images: list[str] | None = None


class PropertyStatusUpdate(BaseModel):
    """Payload for updating property status."""

    status: PropertyStatus


class PropertyFeaturedUpdate(BaseModel):
    """Payload for toggling featured flag."""

    is_featured: bool


class PropertyResponse(BaseModel):
    """Property payload returned to clients."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    agent_id: UUID | None = None
    title: str
    description: str | None = None
    price: Decimal
    currency: str
    type: PropertyType | None = None
    status: PropertyStatus
    operation: PropertyOperation | None = None
    address: str
    city: str | None = None
    state: str | None = None
    bedrooms: int
    bathrooms: int
    area_m2: Decimal | None = None
    images: list[str] | None = None
    is_featured: bool
    created_at: datetime
    updated_at: datetime
