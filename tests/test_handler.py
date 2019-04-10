from http import HTTPStatus

import pytest
from aiohttp import web
from pydantic import BaseModel

import aioapi as api


class TestSimple:
    async def test_simple(self, client_for):
        async def handler():
            return web.json_response({"super": "simple"})

        client = await client_for(routes=[api.get("/test/simple", handler)])
        resp = await client.get("/test/simple")

        assert resp.status == HTTPStatus.OK
        assert await resp.json() == {"super": "simple"}

    async def test_request_and_application(self, client_for):
        async def handler(request: web.Request, app: web.Application):
            return web.json_response({"request": id(request), "app": id(app)})

        client = await client_for(routes=[api.get("/test/reqapp", handler)])
        resp = await client.get("/test/reqapp")

        assert resp.status == HTTPStatus.OK
        result = await resp.json()
        assert isinstance(result["request"], int)
        assert isinstance(result["app"], int)

    @pytest.mark.parametrize(
        "req, resp_status, resp_body",
        (
            (
                {"name": "Walter"},
                HTTPStatus.OK,
                {"user": {"name": "Walter", "age": 42}},
            ),
            (
                {},
                HTTPStatus.BAD_REQUEST,
                {
                    "type": "validation_error",
                    "title": "Your request parameters didn't validate.",
                    "invalid_params": [
                        {
                            "loc": ["body", "name"],
                            "msg": "field required",
                            "type": "value_error.missing",
                        }
                    ],
                },
            ),
            (
                {"name": "Walter", "age": "random"},
                HTTPStatus.BAD_REQUEST,
                {
                    "type": "validation_error",
                    "title": "Your request parameters didn't validate.",
                    "invalid_params": [
                        {
                            "loc": ["body", "age"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer",
                        }
                    ],
                },
            ),
        ),
    )
    async def test_body(self, client_for, req, resp_status, resp_body):
        class User(BaseModel):
            name: str
            age: int = 42

        async def handler(body: api.Body[User]):
            return web.json_response({"user": body.cleaned.dict()})

        client = await client_for(routes=[api.post("/test/body", handler)])
        resp = await client.post("/test/body", json=req)

        assert resp.status == resp_status
        assert await resp.json() == resp_body

    @pytest.mark.parametrize(
        "req, resp_status, resp_body",
        (
            (42, HTTPStatus.OK, {"pp": 42}),
            (
                "string",
                HTTPStatus.BAD_REQUEST,
                {
                    "type": "validation_error",
                    "title": "Your request parameters didn't validate.",
                    "invalid_params": [
                        {
                            "loc": ["path", "pp"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer",
                        }
                    ],
                },
            ),
        ),
    )
    async def test_path_param(self, client_for, req, resp_status, resp_body):
        async def handler(pp: api.PathParam[int]):
            return web.json_response({"pp": pp.cleaned})

        client = await client_for(routes=[api.get("/test/{pp}", handler)])
        resp = await client.get(f"/test/{req}")

        assert resp.status == resp_status
        assert await resp.json() == resp_body

    @pytest.mark.parametrize(
        "req, resp_status, resp_body",
        (
            ({"qp": 42}, HTTPStatus.OK, {"qp": 42, "qpd": "random"}),
            (
                {"qp": "string"},
                HTTPStatus.BAD_REQUEST,
                {
                    "type": "validation_error",
                    "title": "Your request parameters didn't validate.",
                    "invalid_params": [
                        {
                            "loc": ["query", "qp"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer",
                        }
                    ],
                },
            ),
        ),
    )
    async def test_query_param(self, client_for, req, resp_status, resp_body):
        async def handler(
            qp: api.QueryParam[int],
            qpd: api.QueryParam[str] = api.QueryParam("random"),  # noqa: B009
        ):
            return web.json_response({"qp": qp.cleaned, "qpd": qpd.cleaned})

        client = await client_for(routes=[api.get("/test/query", handler)])
        resp = await client.get("/test/query", params=req)

        assert resp.status == resp_status
        assert await resp.json() == resp_body

    @pytest.mark.parametrize(
        "req, resp_status, resp_body",
        (
            (
                {"path": 42, "query": {"qp": 84}, "body": {"name": "Walter"}},
                HTTPStatus.OK,
                {
                    "user": {"name": "Walter", "age": 42},
                    "pp": 42,
                    "qp": 84,
                    "qpd": "random",
                },
            ),
            (
                {"path": 42, "query": {"qp": "random"}, "body": {}},
                HTTPStatus.BAD_REQUEST,
                {
                    "type": "validation_error",
                    "title": "Your request parameters didn't validate.",
                    "invalid_params": [
                        {
                            "loc": ["body", "name"],
                            "msg": "field required",
                            "type": "value_error.missing",
                        },
                        {
                            "loc": ["query", "qp"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer",
                        },
                    ],
                },
            ),
        ),
    )
    async def test_multiple(self, client_for, req, resp_status, resp_body):
        class User(BaseModel):
            name: str
            age: int = 42

        async def handler(
            request: web.Request,
            body: api.Body[User],
            pp: api.PathParam[int],
            qp: api.QueryParam[int],
            qpd: api.QueryParam[str] = api.QueryParam("random"),  # noqa: B009
        ):
            return web.json_response(
                {
                    "user": body.cleaned.dict(),
                    "pp": pp.cleaned,
                    "qp": qp.cleaned,
                    "qpd": qpd.cleaned,
                }
            )

        client = await client_for(routes=[api.put("/test/{pp}", handler)])
        resp = await client.put(
            f"/test/{req['path']}", json=req["body"], params=req["query"]
        )

        assert resp.status == resp_status
        assert await resp.json() == resp_body


class TestCBV:
    async def test_simple(self, client_for):
        class View(web.View):
            async def get(self):
                return web.json_response({"super": "simple"})

        client = await client_for(routes=[api.view("/test/simple", View)])
        resp = await client.get("/test/simple")

        assert resp.status == HTTPStatus.OK
        assert await resp.json() == {"super": "simple"}

    async def test_request_and_application(self, client_for):
        class View(web.View):
            async def get(self, request: web.Request, app: web.Application):
                return web.json_response({"request": id(request), "app": id(app)})

        client = await client_for(routes=[api.view("/test/reqapp", View)])
        resp = await client.get("/test/reqapp")

        assert resp.status == HTTPStatus.OK
        result = await resp.json()
        assert isinstance(result["request"], int)
        assert isinstance(result["app"], int)

    @pytest.mark.parametrize(
        "req, resp_status, resp_body",
        (
            (
                {"name": "Walter"},
                HTTPStatus.OK,
                {"user": {"name": "Walter", "age": 42}},
            ),
            (
                {},
                HTTPStatus.BAD_REQUEST,
                {
                    "type": "validation_error",
                    "title": "Your request parameters didn't validate.",
                    "invalid_params": [
                        {
                            "loc": ["body", "name"],
                            "msg": "field required",
                            "type": "value_error.missing",
                        }
                    ],
                },
            ),
            (
                {"name": "Walter", "age": "random"},
                HTTPStatus.BAD_REQUEST,
                {
                    "type": "validation_error",
                    "title": "Your request parameters didn't validate.",
                    "invalid_params": [
                        {
                            "loc": ["body", "age"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer",
                        }
                    ],
                },
            ),
        ),
    )
    async def test_body(self, client_for, req, resp_status, resp_body):
        class User(BaseModel):
            name: str
            age: int = 42

        class View(web.View):
            async def post(self, body: api.Body[User]):
                return web.json_response({"user": body.cleaned.dict()})

        client = await client_for(routes=[api.view("/test/body", View)])
        resp = await client.post("/test/body", json=req)

        assert resp.status == resp_status
        assert await resp.json() == resp_body

    @pytest.mark.parametrize(
        "req, resp_status, resp_body",
        (
            (42, HTTPStatus.OK, {"pp": 42}),
            (
                "string",
                HTTPStatus.BAD_REQUEST,
                {
                    "type": "validation_error",
                    "title": "Your request parameters didn't validate.",
                    "invalid_params": [
                        {
                            "loc": ["path", "pp"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer",
                        }
                    ],
                },
            ),
        ),
    )
    async def test_path_param(self, client_for, req, resp_status, resp_body):
        class View(web.View):
            async def get(self, pp: api.PathParam[int]):
                return web.json_response({"pp": pp.cleaned})

        client = await client_for(routes=[api.view("/test/{pp}", View)])
        resp = await client.get(f"/test/{req}")

        assert resp.status == resp_status
        assert await resp.json() == resp_body

    @pytest.mark.parametrize(
        "req, resp_status, resp_body",
        (
            ({"qp": 42}, HTTPStatus.OK, {"qp": 42, "qpd": "random"}),
            (
                {"qp": "string"},
                HTTPStatus.BAD_REQUEST,
                {
                    "type": "validation_error",
                    "title": "Your request parameters didn't validate.",
                    "invalid_params": [
                        {
                            "loc": ["query", "qp"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer",
                        }
                    ],
                },
            ),
        ),
    )
    async def test_query_param(self, client_for, req, resp_status, resp_body):
        class View(web.View):
            async def get(
                self,
                qp: api.QueryParam[int],
                qpd: api.QueryParam[str] = api.QueryParam("random"),  # noqa: B009
            ):
                return web.json_response({"qp": qp.cleaned, "qpd": qpd.cleaned})

        client = await client_for(routes=[api.view("/test/query", View)])
        resp = await client.get("/test/query", params=req)

        assert resp.status == resp_status
        assert await resp.json() == resp_body

    @pytest.mark.parametrize(
        "req, resp_status, resp_body",
        (
            (
                {"path": 42, "query": {"qp": 84}, "body": {"name": "Walter"}},
                HTTPStatus.OK,
                {
                    "user": {"name": "Walter", "age": 42},
                    "pp": 42,
                    "qp": 84,
                    "qpd": "random",
                },
            ),
            (
                {"path": 42, "query": {"qp": "random"}, "body": {}},
                HTTPStatus.BAD_REQUEST,
                {
                    "type": "validation_error",
                    "title": "Your request parameters didn't validate.",
                    "invalid_params": [
                        {
                            "loc": ["body", "name"],
                            "msg": "field required",
                            "type": "value_error.missing",
                        },
                        {
                            "loc": ["query", "qp"],
                            "msg": "value is not a valid integer",
                            "type": "type_error.integer",
                        },
                    ],
                },
            ),
        ),
    )
    async def test_multiple(self, client_for, req, resp_status, resp_body):
        class User(BaseModel):
            name: str
            age: int = 42

        class View(web.View):
            async def put(
                self,
                request: web.Request,
                body: api.Body[User],
                pp: api.PathParam[int],
                qp: api.QueryParam[int],
                qpd: api.QueryParam[str] = api.QueryParam("random"),  # noqa: B009
            ):
                return web.json_response(
                    {
                        "user": body.cleaned.dict(),
                        "pp": pp.cleaned,
                        "qp": qp.cleaned,
                        "qpd": qpd.cleaned,
                    }
                )

        client = await client_for(routes=[api.view("/test/{pp}", View)])
        resp = await client.put(
            f"/test/{req['path']}", json=req["body"], params=req["query"]
        )

        assert resp.status == resp_status
        assert await resp.json() == resp_body
