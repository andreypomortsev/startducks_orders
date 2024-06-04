import pytest
from httpx import AsyncClient
from fastapi.testclient import TestClient
from main import app, startup, shutdown


@pytest.fixture(scope="module")
async def test_client():
    await startup()
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
    await shutdown()


def test_read_main():
    with TestClient(app) as client:
        response = client.get("/")
        assert response.status_code == 404  # Adjust based on actual available endpoints


@pytest.mark.asyncio
async def test_create_order(test_client):
    response = await test_client.post("/order", json={"preferences": ["Эспрессо"]})
    assert response.status_code == 200
    assert "Order" in response.json()["result"]


@pytest.mark.asyncio
async def test_create_order_no_drinks_available(test_client):
    response = await test_client.post("/order", json={"preferences": ["UnknownDrink"]})
    assert response.status_code == 200
    assert response.json()["result"] == "К сожалению, не можем предложить Вам напиток"
