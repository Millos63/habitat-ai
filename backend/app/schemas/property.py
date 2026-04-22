from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.models.property import PropertyOperation, PropertyStatus, PropertyType


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
