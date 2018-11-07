from aiohttp import web

from example.application import get_application


def main():
    web.run_app(get_application())


if __name__ == "__main__":
    main()
