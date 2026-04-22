import pytest
from httpx import ASGITransport, AsyncClient

from app.database import engine
from app.main import app


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
async def client():
    """Async test client for the FastAPI application."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    await engine.dispose()
