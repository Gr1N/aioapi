from functools import partial
from http import HTTPStatus
from typing import Awaitable, Callable, Dict, Iterator, Tuple, Union, cast

from aiohttp import web
from aiohttp.web_routedef import _HandlerType
from pydantic import BaseModel, ValidationError

from aioapi.inspect.entities import HandlerMeta
from aioapi.inspect.inspector import HandlerInspector
from aioapi.typedefs import Body, PathParam, QueryParam

__all__ = ("wraps",)

_HandlerParams = Union[Body, PathParam, QueryParam]

_GenRawDataResult = Tuple[str, dict]
_GenRawDataCallable = Callable[[web.Request], Awaitable[_GenRawDataResult]]

_GenKwargsResult = Iterator[Tuple[str, _HandlerParams]]
_GenKwargsCallable = Callable[[BaseModel], _GenKwargsResult]


def wraps(handler: _HandlerType) -> _HandlerType:
    handler_casted = cast(Callable[..., Awaitable], handler)
    handler_meta = HandlerInspector(handler_casted)()

    raw_data_generators = tuple(_gen_raw_data_generators(handler_meta))
    kwargs_generators = tuple(_gen_kwargs_generators(handler_meta))

    async def wrapped(request: web.Request) -> web.StreamResponse:
        raw = {}
        for raw_data_generator in raw_data_generators:
            k, raw_data = await raw_data_generator(request)
            raw[k] = raw_data

        try:
            cleaned = cast(BaseModel, handler_meta.request_type).parse_obj(raw)
        except ValidationError as e:
            return web.json_response(
                {"detail": e.errors()}, status=HTTPStatus.BAD_REQUEST
            )

        kwargs: Dict[str, _HandlerParams] = {}
        for kwargs_generator in kwargs_generators:
            for k, param in kwargs_generator(cleaned):
                kwargs[k] = param

        resp = await handler_casted(**kwargs)

        return resp

    return wrapped if handler_meta.request_type else handler


def _gen_raw_data_generators(meta: HandlerMeta) -> Iterator[_GenRawDataCallable]:
    if meta.request_body_pair:
        yield _gen_body_raw_data

    if meta.request_path_mapping:
        yield _gen_path_raw_data

    if meta.request_query_mapping:
        yield _gen_query_raw_data


async def _gen_body_raw_data(request: web.Request) -> _GenRawDataResult:
    return "body", await request.json()


async def _gen_path_raw_data(request: web.Request) -> _GenRawDataResult:
    return "path", dict(request.match_info)


async def _gen_query_raw_data(request: web.Request) -> _GenRawDataResult:
    return "query", dict(request.query)


def _gen_kwargs_generators(meta: HandlerMeta) -> Iterator[_GenKwargsCallable]:
    if meta.request_body_pair:
        yield partial(_gen_body_kwargs, meta=meta)

    if meta.request_path_mapping:
        yield _gen_path_kwargs

    if meta.request_query_mapping:
        yield _gen_query_kwargs


def _gen_body_kwargs(cleaned: BaseModel, *, meta: HandlerMeta) -> _GenKwargsResult:
    k, _ = cast(tuple, meta.request_body_pair)
    yield k, Body(cleaned.body)  # type: ignore


def _gen_path_kwargs(cleaned: BaseModel) -> _GenKwargsResult:
    for k, v in cleaned.path:  # type: ignore
        yield k, PathParam(v)


def _gen_query_kwargs(cleaned: BaseModel) -> _GenKwargsResult:
    for k, v in cleaned.query:  # type: ignore
        yield k, QueryParam(v)
