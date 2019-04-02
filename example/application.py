from aiohttp import web

import aioapi as api
from example import views

__all__ = ("get_application",)


def get_application():
    app = web.Application()

    app.add_routes(
        [
            web.get("/hello_batman", views.hello_batman),
            api.get("/hello_components", views.hello_components),
            api.get("/hello/{name}", views.hello_path),
            api.get("/hello_query", views.hello_query),
            api.post("/hello_body", views.hello_body),
        ]
    )

    return app
