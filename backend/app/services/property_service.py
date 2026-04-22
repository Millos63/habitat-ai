from decimal import Decimal
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.property import Property, PropertyOperation, PropertyStatus, PropertyType
from app.models.user import User
from app.schemas.property import PropertyCreate
from app.utils.exceptions import ForbiddenError, NotFoundError


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


async def create_property(db: AsyncSession, agent: User, data: PropertyCreate) -> Property:
    """Create a new property listing for an agent."""
    property_obj = Property(
        agent_id=agent.id,
        title=data.title,
        description=data.description,
        price=data.price,
        currency=data.currency.upper(),
        type=data.type,
        operation=data.operation,
        address=data.address,
        city=data.city,
        state=data.state,
        bedrooms=data.bedrooms,
        bathrooms=data.bathrooms,
        area_m2=data.area_m2,
        images=data.images,
    )
    db.add(property_obj)
    await db.commit()
    await db.refresh(property_obj)
    return property_obj


async def get_owned_property_or_raise(
    db: AsyncSession,
    *,
    property_id: UUID,
    user: User,
) -> Property:
    """Fetch a property and ensure the requesting user owns it."""
    property_obj = await get_property_by_id(db, property_id)
    if property_obj is None:
        raise NotFoundError("Property not found")

    if property_obj.agent_id != user.id:
        raise ForbiddenError("You don't have permission to manage this property")

    return property_obj


async def replace_property(
    db: AsyncSession,
    *,
    property_obj: Property,
    data: PropertyCreate,
) -> Property:
    """Replace a property listing data."""
    property_obj.title = data.title
    property_obj.description = data.description
    property_obj.price = data.price
    property_obj.currency = data.currency.upper()
    property_obj.type = data.type
    property_obj.operation = data.operation
    property_obj.address = data.address
    property_obj.city = data.city
    property_obj.state = data.state
    property_obj.bedrooms = data.bedrooms
    property_obj.bathrooms = data.bathrooms
    property_obj.area_m2 = data.area_m2
    property_obj.images = data.images

    await db.commit()
    await db.refresh(property_obj)
    return property_obj


async def delete_property(db: AsyncSession, property_obj: Property) -> None:
    """Delete a property listing."""
    await db.delete(property_obj)
    await db.commit()


async def update_property_status(
    db: AsyncSession,
    *,
    property_obj: Property,
    status: PropertyStatus,
) -> Property:
    """Update property status."""
    property_obj.status = status
    await db.commit()
    await db.refresh(property_obj)
    return property_obj


async def update_property_featured(
    db: AsyncSession,
    *,
    property_obj: Property,
    is_featured: bool,
) -> Property:
    """Update property featured flag."""
    property_obj.is_featured = is_featured
    await db.commit()
    await db.refresh(property_obj)
    return property_obj
