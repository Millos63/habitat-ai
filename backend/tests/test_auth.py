from uuid import uuid4

import pytest


@pytest.mark.anyio
async def test_register_login_and_me_flow(client):
    email = f"test-{uuid4()}@example.com"
    password = "Password123"

    register_response = await client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": password,
            "full_name": "Test User",
            "role": "client",
        },
    )

    assert register_response.status_code == 201
    register_data = register_response.json()
    assert "access_token" in register_data
    assert register_data["token_type"] == "bearer"
    assert "user_id" in register_data

    login_response = await client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert login_response.status_code == 200
    login_data = login_response.json()
    assert "access_token" in login_data

    me_response = await client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {login_data['access_token']}"},
    )
    assert me_response.status_code == 200
    me_data = me_response.json()
    assert me_data["email"] == email
    assert me_data["role"] == "client"


@pytest.mark.anyio
async def test_register_duplicate_email_returns_conflict(client):
    email = f"duplicate-{uuid4()}@example.com"
    payload = {
        "email": email,
        "password": "Password123",
        "full_name": "Duplicate User",
        "role": "client",
    }

    first = await client.post("/api/auth/register", json=payload)
    assert first.status_code == 201

    second = await client.post("/api/auth/register", json=payload)
    assert second.status_code == 409
    assert second.json()["detail"] == "Email is already registered"


@pytest.mark.anyio
async def test_login_with_invalid_credentials_returns_unauthorized(client):
    email = f"invalid-{uuid4()}@example.com"

    register_response = await client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "Password123",
            "full_name": "Invalid Login User",
            "role": "client",
        },
    )
    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/auth/login",
        json={"email": email, "password": "WrongPass123"},
    )
    assert login_response.status_code == 401
    assert login_response.json()["detail"] == "Invalid email or password"


@pytest.mark.anyio
async def test_me_without_token_returns_unauthorized(client):
    response = await client.get("/api/auth/me")
    assert response.status_code == 401


@pytest.mark.anyio
async def test_register_weak_password_returns_validation_error(client):
    email = f"weak-{uuid4()}@example.com"

    response = await client.post(
        "/api/auth/register",
        json={
            "email": email,
            "password": "password123",
            "full_name": "Weak Password",
            "role": "client",
        },
    )

    assert response.status_code == 422
    detail = response.json()["detail"]
    assert any("uppercase" in item.get("msg", "").lower() for item in detail)
