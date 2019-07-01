from aiopg.sa import create_engine

from service_api.config import select_db_config


async def select_statement(statement):
    async with create_engine(**select_db_config()) as engine:
        async with engine.acquire() as conn:
            result = [dict(r) async for r in conn.execute(statement)]
            return result[0] if len(result) == 1 else result


async def execute_statement(statement):
    async with create_engine(**select_db_config()) as engine:
        async with engine.acquire() as conn:
            await conn.execute(statement)
