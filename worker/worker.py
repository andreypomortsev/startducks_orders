import asyncio
import redis.asyncio as redis
import asyncpg
import json

recipes = {
    "Эспрессо": {"coffee": 1, "milk": 0, "cream": 0},
    "Капучино": {"coffee": 1, "milk": 3, "cream": 0},
    "Макиато": {"coffee": 2, "milk": 1, "cream": 0},
    "Кофе по-венски": {"coffee": 1, "milk": 0, "cream": 2},
    "Латте Макиато": {"coffee": 1, "milk": 2, "cream": 1},
    "Кон Панна": {"coffee": 1, "milk": 0, "cream": 1},
}

async def check_ingredients(conn, ingredients: dict) -> bool:
    async with conn.transaction():
        for ingredient, quantity in ingredients.items():
            result = await conn.fetchval(
                "SELECT quantity FROM in_stock WHERE ingredient = $1 FOR UPDATE",
                ingredient,
            )
            if result is None or result < quantity:
                return False
    return True

async def update_stock(conn, ingredients: dict) -> None:
    async with conn.transaction():
        for ingredient, quantity in ingredients.items():
            await conn.execute(
                "UPDATE in_stock SET quantity = quantity - $1 WHERE ingredient = $2",
                quantity,
                ingredient,
            )

async def process_order(order_data: dict, db_pool, redis_conn):
    async with db_pool.acquire() as conn:
        for drink in order_data["preferences"]:
            ingredients = recipes.get(drink, False)
            if ingredients and await check_ingredients(conn, ingredients):
                await update_stock(conn, ingredients)
                return f"Order {order_data['order_id']}: {drink} prepared"
    return f"Order {order_data['order_id']}: No available drinks"

async def worker():
    redis_conn = redis.from_url("redis://redis")
    db_pool = await asyncpg.create_pool(dsn="postgresql://user:password@db/mydatabase")
    while True:
        order_data_json = await redis_conn.blpop("orders_queue")
        order_data = json.loads(order_data_json[1])
        result = await process_order(order_data, db_pool, redis_conn)
        print(result)  # Here you might update the order status or send a notification

loop = asyncio.get_event_loop()
loop.run_until_complete(worker())
