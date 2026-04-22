from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.property import PropertyOperation, PropertyType
from app.models.user import User, UserRole
from app.routers.auth import get_current_user
from app.schemas.property import (
    PropertyCreate,
    PropertyFeaturedUpdate,
    PropertyResponse,
    PropertyStatusUpdate,
)
from app.services.property_service import (
    create_property,
    delete_property,
    get_property_by_id,
    get_owned_property_or_raise,
    list_featured_properties,
    list_properties,
    replace_property,
    update_property_featured,
    update_property_status,
)
from app.utils.exceptions import ForbiddenError, NotFoundError

router = APIRouter(prefix="/api/properties", tags=["properties"])


def ensure_agent_role(user: User) -> None:
    """Ensure the current user has agent permissions."""
    if user.role not in {UserRole.AGENT, UserRole.ADMIN}:
        raise ForbiddenError("Only agents can manage property listings")


@router.get("", response_model=list[PropertyResponse])
async def list_properties_endpoint(
    response: Response,
    operation: PropertyOperation | None = Query(default=None),
    type: PropertyType | None = Query(default=None),
    city: str | None = Query(default=None),
    min_price: Decimal | None = Query(default=None, ge=0),
    max_price: Decimal | None = Query(default=None, ge=0),
    min_bedrooms: int | None = Query(default=None, ge=0),
    min_bathrooms: int | None = Query(default=None, ge=0),
    min_area: Decimal | None = Query(default=None, ge=0),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
) -> list[PropertyResponse]:
    """List properties with pagination and optional filters."""
    properties, total = await list_properties(
        db,
        operation=operation,
        property_type=type,
        city=city,
        min_price=min_price,
        max_price=max_price,
        min_bedrooms=min_bedrooms,
        min_bathrooms=min_bathrooms,
        min_area=min_area,
        page=page,
        limit=limit,
    )
    response.headers["X-Total-Count"] = str(total)
    return [PropertyResponse.model_validate(property_obj) for property_obj in properties]


@router.get("/featured", response_model=list[PropertyResponse])
async def featured_properties_endpoint(
    limit: int = Query(default=10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
) -> list[PropertyResponse]:
    """List featured active properties."""
    properties = await list_featured_properties(db, limit=limit)
    return [PropertyResponse.model_validate(property_obj) for property_obj in properties]


@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property_endpoint(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> PropertyResponse:
    """Get a single property by id."""
    property_obj = await get_property_by_id(db, property_id)
    if property_obj is None:
        raise NotFoundError("Property not found")

    return PropertyResponse.model_validate(property_obj)


@router.post("", response_model=PropertyResponse, status_code=201)
async def create_property_endpoint(
    data: PropertyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PropertyResponse:
    """Create a new property listing."""
    ensure_agent_role(current_user)
    property_obj = await create_property(db, current_user, data)
    return PropertyResponse.model_validate(property_obj)


@router.put("/{property_id}", response_model=PropertyResponse)
async def replace_property_endpoint(
    property_id: UUID,
    data: PropertyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PropertyResponse:
    """Replace an existing property listing."""
    ensure_agent_role(current_user)
    property_obj = await get_owned_property_or_raise(db, property_id=property_id, user=current_user)
    updated_property = await replace_property(db, property_obj=property_obj, data=data)
    return PropertyResponse.model_validate(updated_property)


@router.delete("/{property_id}")
async def delete_property_endpoint(
    property_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> dict[str, str]:
    """Delete an existing property listing."""
    ensure_agent_role(current_user)
    property_obj = await get_owned_property_or_raise(db, property_id=property_id, user=current_user)
    await delete_property(db, property_obj)
    return {"message": "Property deleted successfully"}


@router.patch("/{property_id}/status", response_model=PropertyResponse)
async def update_property_status_endpoint(
    property_id: UUID,
    data: PropertyStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PropertyResponse:
    """Update property status."""
    ensure_agent_role(current_user)
    property_obj = await get_owned_property_or_raise(db, property_id=property_id, user=current_user)
    updated_property = await update_property_status(db, property_obj=property_obj, status=data.status)
    return PropertyResponse.model_validate(updated_property)


@router.patch("/{property_id}/featured", response_model=PropertyResponse)
async def update_property_featured_endpoint(
    property_id: UUID,
    data: PropertyFeaturedUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> PropertyResponse:
    """Update property featured flag."""
    ensure_agent_role(current_user)
    property_obj = await get_owned_property_or_raise(db, property_id=property_id, user=current_user)
    updated_property = await update_property_featured(
        db,
        property_obj=property_obj,
        is_featured=data.is_featured,
    )
    return PropertyResponse.model_validate(updated_property)
