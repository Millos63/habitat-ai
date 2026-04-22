from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, Query, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.property import PropertyOperation, PropertyType
from app.schemas.property import PropertyResponse
from app.services.property_service import (
    get_property_by_id,
    list_featured_properties,
    list_properties,
)
from app.utils.exceptions import NotFoundError

router = APIRouter(prefix="/api/properties", tags=["properties"])


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
