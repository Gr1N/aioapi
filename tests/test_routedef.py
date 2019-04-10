from http import HTTPStatus

import pytest
from aiohttp import web

import aioapi as api


@pytest.mark.parametrize(
    "method", ("head", "options", "post", "put", "patch", "delete")
)
async def test_simple(client_for, method):
    async def handler():
        return web.json_response({"super": "simple"})

    route = getattr(api, method)("/test/simple", handler)
    client = await client_for(routes=[route])

    req = getattr(client, method)
    resp = await req("/test/simple")

    assert resp.status == HTTPStatus.OK


async def test_view(client_for):
    class View(web.View):
        async def get(self):
            return web.json_response({})

        async def post(self):
            return web.json_response({})

    client = await client_for(routes=[api.view("/test/view", View)])

    resp = await client.get("/test/view")
    assert resp.status == HTTPStatus.OK

    resp = await client.post("/test/view")
    assert resp.status == HTTPStatus.OK
