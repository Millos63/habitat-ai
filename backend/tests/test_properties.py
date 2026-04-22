from decimal import Decimal
from uuid import uuid4

import pytest

from app.database import async_session
from app.models.property import Property, PropertyOperation, PropertyStatus, PropertyType
from app.models.user import User, UserRole
from app.utils.security import hash_password


async def seed_property(*, title: str, city: str, is_featured: bool, status: PropertyStatus) -> str:
    """Create and persist a property for tests."""
    async with async_session() as session:
        user = User(
            email=f"agent-{uuid4()}@example.com",
            password_hash=hash_password("Password123"),
            full_name="Agent User",
            role=UserRole.AGENT,
        )
        session.add(user)
        await session.flush()

        property_obj = Property(
            agent_id=user.id,
            title=title,
            description="Test listing",
            price=Decimal("2500000.00"),
            currency="MXN",
            type=PropertyType.HOUSE,
            status=status,
            operation=PropertyOperation.SALE,
            address="Test Street 123",
            city=city,
            state="CDMX",
            bedrooms=3,
            bathrooms=2,
            area_m2=Decimal("120.00"),
            images=["https://example.com/image-1.jpg"],
            is_featured=is_featured,
        )
        session.add(property_obj)
        await session.commit()
        await session.refresh(property_obj)
        return str(property_obj.id)


@pytest.mark.anyio
async def test_list_properties_returns_only_active_and_sets_total_header(client):
    await seed_property(title=f"Active {uuid4()}", city="Monterrey", is_featured=False, status=PropertyStatus.ACTIVE)
    await seed_property(title=f"Paused {uuid4()}", city="Monterrey", is_featured=False, status=PropertyStatus.PAUSED)

    response = await client.get("/api/properties", params={"city": "Monterrey", "page": 1, "limit": 20})

    assert response.status_code == 200
    assert response.headers.get("X-Total-Count") is not None

    data = response.json()
    assert len(data) >= 1
    assert all(item["status"] == "active" for item in data)


@pytest.mark.anyio
async def test_get_property_detail_returns_property(client):
    property_id = await seed_property(
        title=f"Detail {uuid4()}",
        city="Guadalajara",
        is_featured=True,
        status=PropertyStatus.ACTIVE,
    )

    response = await client.get(f"/api/properties/{property_id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == property_id
    assert data["city"] == "Guadalajara"


@pytest.mark.anyio
async def test_get_property_detail_returns_404_when_missing(client):
    response = await client.get(f"/api/properties/{uuid4()}")

    assert response.status_code == 404
    assert response.json()["detail"] == "Property not found"


@pytest.mark.anyio
async def test_featured_properties_returns_only_featured(client):
    await seed_property(title=f"Featured {uuid4()}", city="Puebla", is_featured=True, status=PropertyStatus.ACTIVE)
    await seed_property(title=f"Regular {uuid4()}", city="Puebla", is_featured=False, status=PropertyStatus.ACTIVE)

    response = await client.get("/api/properties/featured")

    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert all(item["is_featured"] is True for item in data)
