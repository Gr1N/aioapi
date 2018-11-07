from aiohttp import web

from example.views import HandsomeView, UglyView

__all__ = ("get_application",)


def get_application():
    app = web.Application()

    app.router.add_view("/handsome", HandsomeView)
    app.router.add_view("/ugly", UglyView)

    return app
