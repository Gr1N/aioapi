from aiohttp import web

import aiohttp_typed_views as tpd

__all__ = ("hello_batman", "hello_path")


async def hello_batman(request):
    return web.json_response({"whoami": "I'm Batman!"})


async def hello_path(name: tpd.PathParam[str]):
    return web.json_response({"whoami": name.cleaned})
