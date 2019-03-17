from aiohttp import web

import aiohttp_typed_views as tpd
from example import views

__all__ = ("get_application",)


def get_application():
    app = web.Application()

    app.add_routes(
        [
            web.get("/hello_batman", views.hello_batman),
            tpd.get("/hello/{name}", views.hello_path),
        ]
    )

    return app
