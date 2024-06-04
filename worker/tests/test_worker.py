import pytest
import aioredis
import asyncpg
from worker import process_order, check_ingredients, update_stock, recipes


@pytest.fixture
async def test_redis():
    redis = await aioredis.create_redis_pool("redis://localhost")
    yield redis
    redis.close()
    await redis.wait_closed()


@pytest.fixture
async def test_db():
    db_pool = await asyncpg.create_pool(
        dsn="postgresql://user:password@localhost/mydatabase"
    )
    yield db_pool
    await db_pool.close()


@pytest.fixture
async def setup_db(test_db):
    async with test_db.acquire() as conn:
        await conn.execute("TRUNCATE TABLE in_stock RESTART IDENTITY")
        for ingredient, quantity in recipes["Эспрессо"].items():
            await conn.execute(
                "INSERT INTO in_stock (ingredient, quantity) VALUES ($1, $2)",
                ingredient,
                quantity,
            )


@pytest.mark.asyncio
async def test_process_order_success(setup_db, test_redis, test_db):
    order_data = {"order_id": "1", "preferences": ["Эспрессо"]}
    result = await process_order(order_data, test_db, test_redis)
    assert result == "Order 1: Эспрессо prepared"


@pytest.mark.asyncio
async def test_process_order_insufficient_ingredients(test_redis, test_db):
    order_data = {"order_id": "2", "preferences": ["Эспрессо"]}
    result = await process_order(order_data, test_db, test_redis)
    assert result == "Order 2: No available drinks"
