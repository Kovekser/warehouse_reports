import os
import asyncio
from aiopg.sa import create_engine

from tests import BaseTestCase
from service_api.config import select_db_config
from commands import InitDB


class BaseDomainTest(BaseTestCase):

    @classmethod
    def setUpClass(cls):
        cls.my_loop = asyncio.get_event_loop()
        cls.my_loop.run_until_complete(InitDB('test_db').create_db())

    @classmethod
    def tearDownClass(cls):
        cls.my_loop = asyncio.get_event_loop()
        cls.my_loop.run_until_complete(InitDB('test_db').remove_test_db())

    async def test_get_all_tables(self):
        statement = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' ;"
        table = 'report_status'
        async with create_engine(**select_db_config()) as engine:
            async with engine.acquire() as conn:
                result = [list(dict(r).values())[0]
                          async for r in conn.execute(statement)]
        self.assertEqual(len(result), 3)
        self.assertIn(table, result)
