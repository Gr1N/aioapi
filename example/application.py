from aiohttp import web

__all__ = ("get_application",)


def get_application():
    app = web.Application()

    return app
