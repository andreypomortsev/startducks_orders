import pytest
import redis.asyncio as redis
import asyncpg
from worker import process_order

@pytest.fixture
async def test_redis():
    redis_conn = redis.from_url("redis://localhost")
    await redis_conn.flushall()  # Clear Redis for testing
    yield redis_conn
    await redis_conn.close()

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
        await conn.execute("""
            INSERT INTO in_stock (ingredient, quantity) VALUES
            ('coffee', 10),
            ('milk', 10),
            ('cream', 10)
        """)
    yield

@pytest.mark.asyncio
async def test_process_order_success(setup_db, test_redis, test_db):
    order_data = {"order_id": "1", "preferences": ["Эспрессо"]}
    result = await process_order(order_data, test_db, test_redis)
    assert result == "Order 1: Эспрессо prepared"

@pytest.mark.asyncio
async def test_process_order_insufficient_ingredients(test_db, test_redis):
    async with test_db.acquire() as conn:
        await conn.execute("TRUNCATE TABLE in_stock RESTART IDENTITY")
        await conn.execute("INSERT INTO in_stock (ingredient, quantity) VALUES ('coffee', 0)")

    order_data = {"order_id": "2", "preferences": ["Эспрессо"]}
    result = await process_order(order_data, test_db, test_redis)
    assert result == "Order 2: No available drinks"
