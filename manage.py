import asyncio

from commands import runserver, InitDB


def main():
    my_loop = asyncio.get_event_loop()
    my_loop.run_until_complete(InitDB('whreports').create_db())
    runserver()


if __name__ == '__main__':
    main()
