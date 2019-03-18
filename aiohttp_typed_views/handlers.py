from http import HTTPStatus
from typing import Awaitable, Callable, Dict, Union, cast

from aiohttp import web
from aiohttp.web_routedef import _HandlerType
from pydantic import ValidationError

from aiohttp_typed_views.inspect import HandlerInspector
from aiohttp_typed_views.typedefs import PathParam, QueryParam

__all__ = ("wraps",)


def wraps(handler: _HandlerType) -> _HandlerType:
    handler_casted = cast(Callable[..., Awaitable], handler)
    handler_meta = HandlerInspector(handler_casted)()

    async def wrapped(request: web.Request) -> web.StreamResponse:
        raw = {}
        if handler_meta.request_with_path:
            raw["path"] = dict(request.match_info)
        if handler_meta.request_with_query:
            raw["query"] = dict(request.query)

        try:
            cleaned = handler_meta.request_type.parse_obj(raw)
        except ValidationError as e:
            return web.json_response(
                {"detail": e.errors()}, status=HTTPStatus.BAD_REQUEST
            )

        kwargs: Dict[str, Union[PathParam, QueryParam]] = {}
        if handler_meta.request_with_path:
            for k, v in cleaned.path:  # type: ignore
                kwargs[k] = PathParam(v)
        if handler_meta.request_with_query:
            for k, v in cleaned.query:  # type: ignore
                kwargs[k] = QueryParam(v)

        resp = await handler_casted(**kwargs)

        return resp

    return wrapped
