from aiohttp import web

import aiohttp_typed_views as tpd

__all__ = ("hello_batman", "hello_path", "hello_query")


DEFAULT_AGE_QUERY_PARAM = tpd.QueryParam(27)


async def hello_batman(request):
    return web.json_response({"whoami": "I'm Batman!"})


async def hello_path(name: tpd.PathParam[str]):
    return web.json_response({"whoami": name.cleaned})


async def hello_query(
    name: tpd.QueryParam[str], age: tpd.QueryParam[int] = DEFAULT_AGE_QUERY_PARAM
):
    return web.json_response({"whoami": name.cleaned, "age": age.cleaned})
