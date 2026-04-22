from decimal import Decimal
from uuid import uuid4

import pytest

from app.database import async_session
from app.models.property import Property, PropertyOperation, PropertyStatus, PropertyType
from app.models.user import User, UserRole
from app.utils.security import hash_password


async def register_user(client, *, role: str) -> tuple[str, str]:
    """Register a user and return (token, user_id)."""
    email = f"{role}-{uuid4()}@example.com"
    response = await client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "Password123",
            "full_name": f"{role.title()} User",
            "role": role,
        },
    )
    assert response.status_code == 201
    data = response.json()
    return data["access_token"], data["user_id"]


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


def property_payload() -> dict:
    """Return a valid property create/update payload."""
    return {
        "title": f"Listing {uuid4()}",
        "description": "Nice property",
        "price": "3500000.00",
        "currency": "mxn",
        "type": "house",
        "operation": "sale",
        "address": "Main Street 123",
        "city": "Monterrey",
        "state": "Nuevo Leon",
        "bedrooms": 3,
        "bathrooms": 2,
        "area_m2": "145.00",
        "images": ["https://example.com/p1.jpg"],
    }


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


@pytest.mark.anyio
async def test_create_property_requires_agent_role(client):
    token, _ = await register_user(client, role="client")

    response = await client.post(
        "/api/properties",
        json=property_payload(),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 403
    assert response.json()["detail"] == "Only agents can manage property listings"


@pytest.mark.anyio
async def test_create_property_as_agent_returns_created(client):
    token, user_id = await register_user(client, role="agent")

    response = await client.post(
        "/api/properties",
        json=property_payload(),
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 201
    data = response.json()
    assert data["agent_id"] == user_id
    assert data["currency"] == "MXN"


@pytest.mark.anyio
async def test_replace_property_requires_owner(client):
    owner_token, _ = await register_user(client, role="agent")
    other_token, _ = await register_user(client, role="agent")

    create_response = await client.post(
        "/api/properties",
        json=property_payload(),
        headers={"Authorization": f"Bearer {owner_token}"},
    )
    assert create_response.status_code == 201
    property_id = create_response.json()["id"]

    payload = property_payload()
    payload["title"] = "Updated by other agent"

    replace_response = await client.put(
        f"/api/properties/{property_id}",
        json=payload,
        headers={"Authorization": f"Bearer {other_token}"},
    )

    assert replace_response.status_code == 403
    assert replace_response.json()["detail"] == "You don't have permission to manage this property"


@pytest.mark.anyio
async def test_update_status_and_featured_and_delete_flow(client):
    token, _ = await register_user(client, role="agent")

    create_response = await client.post(
        "/api/properties",
        json=property_payload(),
        headers={"Authorization": f"Bearer {token}"},
    )
    assert create_response.status_code == 201
    property_id = create_response.json()["id"]

    status_response = await client.patch(
        f"/api/properties/{property_id}/status",
        json={"status": "paused"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "paused"

    featured_response = await client.patch(
        f"/api/properties/{property_id}/featured",
        json={"is_featured": True},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert featured_response.status_code == 200
    assert featured_response.json()["is_featured"] is True

    delete_response = await client.delete(
        f"/api/properties/{property_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Property deleted successfully"

    detail_response = await client.get(f"/api/properties/{property_id}")
    assert detail_response.status_code == 404
