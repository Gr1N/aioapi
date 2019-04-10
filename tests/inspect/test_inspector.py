import pytest
from aiohttp import web
from pydantic import BaseModel

from aioapi import Body, PathParam, QueryParam
from aioapi.inspect.exceptions import (
    HandlerMultipleBodyError,
    HandlerParamUnknownTypeError,
)
from aioapi.inspect.inspector import HandlerInspector


class TestInspector:
    def test_unknown_param_type(self):
        async def handler(unknown: int):
            pass

        with pytest.raises(HandlerParamUnknownTypeError) as exc_info:
            HandlerInspector(handler=handler)()
        assert exc_info.value.handler == "test_inspector.handler"
        assert exc_info.value.param == "unknown"

    def test_skip_param(self):
        async def handler(self):
            pass

        meta = HandlerInspector(handler=handler)()
        assert meta.name == "test_inspector.handler"
        assert meta.components_mapping is None
        assert meta.request_type is None
        assert meta.request_body_pair is None
        assert meta.request_path_mapping is None
        assert meta.request_query_mapping is None

    def test_request_and_application(self):
        async def handler(request: web.Request, app: web.Application):
            pass

        meta = HandlerInspector(handler=handler)()
        assert meta.name == "test_inspector.handler"
        assert meta.components_mapping == {
            "request": web.Request,
            "app": web.Application,
        }
        assert meta.request_type is None
        assert meta.request_body_pair is None
        assert meta.request_path_mapping is None
        assert meta.request_query_mapping is None

    def test_body(self):
        async def handler(b: Body[int]):
            pass

        meta = HandlerInspector(handler=handler)()
        assert meta.name == "test_inspector.handler"
        assert meta.components_mapping is None
        assert issubclass(meta.request_type, BaseModel)
        assert meta.request_body_pair == ("b", (int, ...))
        assert meta.request_path_mapping is None
        assert meta.request_query_mapping is None

    def test_body_default(self):
        async def handler(b: Body[int] = Body(42)):  # noqa: B009
            pass

        meta = HandlerInspector(handler=handler)()
        assert meta.name == "test_inspector.handler"
        assert meta.components_mapping is None
        assert issubclass(meta.request_type, BaseModel)
        assert meta.request_body_pair == ("b", (int, 42))
        assert meta.request_path_mapping is None
        assert meta.request_query_mapping is None

    def test_body_multiple(self):
        async def handler(b1: Body[int], b2: Body[str]):
            pass

        with pytest.raises(HandlerMultipleBodyError) as exc_info:
            HandlerInspector(handler=handler)()
        assert exc_info.value.handler == "test_inspector.handler"
        assert exc_info.value.param == "b2"

    def test_path_param(self):
        async def handler(
            pp: PathParam[int], ppd: PathParam[float] = PathParam(5.1)  # noqa: B009
        ):
            pass

        meta = HandlerInspector(handler=handler)()
        assert meta.name == "test_inspector.handler"
        assert meta.components_mapping is None
        assert issubclass(meta.request_type, BaseModel)
        assert meta.request_body_pair is None
        assert meta.request_path_mapping == {"pp": (int, ...), "ppd": (float, ...)}
        assert meta.request_query_mapping is None

    def test_query_param(self):
        async def handler(
            qp: QueryParam[str], qpd: QueryParam[bool] = QueryParam(False)  # noqa: B009
        ):
            pass

        meta = HandlerInspector(handler=handler)()
        assert meta.name == "test_inspector.handler"
        assert meta.components_mapping is None
        assert issubclass(meta.request_type, BaseModel)
        assert meta.request_body_pair is None
        assert meta.request_path_mapping is None
        assert meta.request_query_mapping == {"qp": (str, ...), "qpd": (bool, False)}

    def test_multiple(self):
        async def handler(
            request: web.Request,
            b: Body[int],
            pp: PathParam[int],
            qp: QueryParam[str],
            qpd: QueryParam[bool] = QueryParam(False),  # noqa: B009
        ):
            pass

        meta = HandlerInspector(handler=handler)()
        assert meta.name == "test_inspector.handler"
        assert meta.components_mapping == {"request": web.Request}
        assert issubclass(meta.request_type, BaseModel)
        assert meta.request_body_pair == ("b", (int, ...))
        assert meta.request_path_mapping == {"pp": (int, ...)}
        assert meta.request_query_mapping == {"qp": (str, ...), "qpd": (bool, False)}
