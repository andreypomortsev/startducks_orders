from fastapi import FastAPI
from pydantic import BaseModel
import redis.asyncio as redis
import asyncpg
import json
import uuid

app = FastAPI()


class OrderRequest(BaseModel):
    preferences: list[str]


class OrderResponse(BaseModel):
    result: str


# Initialize Redis and PostgreSQL connections
redis_conn = None
db_pool = None


@app.on_event("startup")
async def startup():
    global redis_conn, db_pool
    redis_conn = redis.from_url("redis://redis")
    db_pool = await asyncpg.create_pool(dsn="postgresql://user:password@db/mydatabase")


@app.on_event("shutdown")
async def shutdown():
    await redis_conn.close()
    await db_pool.close()


@app.post("/order", response_model=OrderResponse)
async def create_order(order_request: OrderRequest):
    order_id = str(uuid.uuid4())
    order_data = {"order_id": order_id, "preferences": order_request.preferences}
    await redis_conn.rpush("orders_queue", json.dumps(order_data))
    return OrderResponse(result=f"Order {order_id} received")
