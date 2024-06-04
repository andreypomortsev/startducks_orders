from fastapi import FastAPI
from pydantic import BaseModel
import aioredis
import asyncpg
import json
import uuid

app = FastAPI()


class OrderRequest(BaseModel):
    preferences: list[str]


class OrderResponse(BaseModel):
    result: str


# Initialize Redis and PostgreSQL connections
redis = None
db_pool = None


@app.event("startup")
async def startup():
    global redis, db_pool
    redis = await aioredis.create_redis_pool("redis://redis")
    db_pool = await asyncpg.create_pool(dsn="postgresql://user:password@db/mydatabase")


@app.event("shutdown")
async def shutdown():
    redis.close()
    await redis.wait_closed()
    await db_pool.close()


@app.post("/order", response_model=OrderResponse)
async def create_order(order_request: OrderRequest):
    order_id = str(uuid.uuid4())
    order_data = {"order_id": order_id, "preferences": order_request.preferences}
    await redis.rpush("orders_queue", json.dumps(order_data))
    return OrderResponse(result=f"Order {order_id} received")
