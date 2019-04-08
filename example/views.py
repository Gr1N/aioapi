from aiohttp import web

from aioapi import Body, PathParam, QueryParam
from example.schemas import HelloBodyRequest

__all__ = (
    "HelloView",
    "hello_batman",
    "hello_components",
    "hello_body",
    "hello_path",
    "hello_query",
)


DEFAULT_AGE_QUERY_PARAM = QueryParam(27)


class HelloView(web.View):
    async def get(
        self, name: QueryParam[str], age: QueryParam[int] = DEFAULT_AGE_QUERY_PARAM
    ):
        return web.json_response({"whoami": name.cleaned, "age": age.cleaned})

    async def post(self, request: web.Request, body: Body[HelloBodyRequest]):
        cleaned = body.cleaned
        return web.json_response(
            {"whoami": cleaned.name, "age": cleaned.age, "whoareyou": id(request)}
        )


async def hello_batman(request):
    return web.json_response({"whoami": "I'm Batman!"})


async def hello_components(request: web.Request, app: web.Application):
    return web.json_response({"whoami": id(request), "whoareyou": id(app)})


async def hello_body(body: Body[HelloBodyRequest]):
    cleaned = body.cleaned
    return web.json_response({"whoami": cleaned.name, "age": cleaned.age})


async def hello_path(name: PathParam[str]):
    return web.json_response({"whoami": name.cleaned})


async def hello_query(
    name: QueryParam[str], age: QueryParam[int] = DEFAULT_AGE_QUERY_PARAM
):
    return web.json_response({"whoami": name.cleaned, "age": age.cleaned})
