import asyncio

from commands import runserver, InitDB
from service_api.config import DEFAULT_SERVICE_NAME


def main():
    my_loop = asyncio.get_event_loop()
    my_loop.run_until_complete(InitDB(DEFAULT_SERVICE_NAME).create_db())
    runserver()


if __name__ == '__main__':
    main()
