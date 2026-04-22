from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property import Property, PropertyOperation, PropertyStatus, PropertyType


async def list_properties(
    db: AsyncSession,
    *,
    operation: PropertyOperation | None,
    property_type: PropertyType | None,
    city: str | None,
    min_price: Decimal | None,
    max_price: Decimal | None,
    min_bedrooms: int | None,
    min_bathrooms: int | None,
    min_area: Decimal | None,
    page: int,
    limit: int,
) -> tuple[list[Property], int]:
    """List active properties using optional filters with pagination."""
    conditions = [Property.status == PropertyStatus.ACTIVE]

    if operation is not None:
        conditions.append(Property.operation == operation)
    if property_type is not None:
        conditions.append(Property.type == property_type)
    if city:
        conditions.append(func.lower(Property.city) == city.strip().lower())
    if min_price is not None:
        conditions.append(Property.price >= min_price)
    if max_price is not None:
        conditions.append(Property.price <= max_price)
    if min_bedrooms is not None:
        conditions.append(Property.bedrooms >= min_bedrooms)
    if min_bathrooms is not None:
        conditions.append(Property.bathrooms >= min_bathrooms)
    if min_area is not None:
        conditions.append(Property.area_m2 >= min_area)

    total = await db.scalar(select(func.count(Property.id)).where(*conditions))

    offset = (page - 1) * limit
    query = (
        select(Property)
        .where(*conditions)
        .order_by(Property.is_featured.desc(), Property.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    result = await db.scalars(query)

    return list(result.all()), int(total or 0)


async def list_featured_properties(db: AsyncSession, limit: int = 10) -> list[Property]:
    """List active featured properties."""
    query = (
        select(Property)
        .where(Property.status == PropertyStatus.ACTIVE, Property.is_featured.is_(True))
        .order_by(Property.created_at.desc())
        .limit(limit)
    )
    result = await db.scalars(query)
    return list(result.all())


async def get_property_by_id(db: AsyncSession, property_id: UUID) -> Property | None:
    """Return a property by id."""
    return await db.get(Property, property_id)
