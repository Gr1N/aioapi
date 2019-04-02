import json
from functools import partial
from typing import Awaitable, Callable, Dict, Iterator, Tuple, Union, cast

from aiohttp import web
from aiohttp.web_routedef import _HandlerType
from pydantic import BaseModel, ValidationError

from aioapi.inspect.entities import HandlerMeta
from aioapi.inspect.inspector import HandlerInspector, param_of
from aioapi.typedefs import Body, PathParam, QueryParam

__all__ = ("wraps",)

_HandlerParams = Union[Body, PathParam, QueryParam, web.Application, web.Request]

_GenRawDataResult = Tuple[str, dict]
_GenRawDataCallable = Callable[[web.Request], Awaitable[_GenRawDataResult]]

_GenKwargsResult = Iterator[Tuple[str, _HandlerParams]]
_GenKwargsCallable = Callable[[BaseModel], _GenKwargsResult]


def wraps(handler: _HandlerType) -> _HandlerType:
    handler_casted = cast(Callable[..., Awaitable], handler)
    handler_meta = HandlerInspector(handler_casted)()

    raw_data_generators = tuple(_gen_raw_data_generators(handler_meta))
    validated_data_generators = tuple(_gen_validated_data_generators(handler_meta))

    def compose(request: web.Request) -> Dict[str, _HandlerParams]:
        composed: Dict[str, _HandlerParams] = {}
        if handler_meta.components_mapping is None:
            return composed

        for k, type_ in handler_meta.components_mapping.items():
            if param_of(type_=type_, is_=web.Application):
                composed[k] = request.app
            elif param_of(type_=type_, is_=web.Request):
                composed[k] = request

        return composed

    async def validate(request: web.Request) -> Dict[str, _HandlerParams]:
        validated: Dict[str, _HandlerParams] = {}
        if handler_meta.request_type is None:
            return validated

        raw = {}
        for raw_data_generator in raw_data_generators:
            k, raw_data = await raw_data_generator(request)
            raw[k] = raw_data

        try:
            cleaned = cast(BaseModel, handler_meta.request_type).parse_obj(raw)
        except ValidationError as e:
            await raise_on_validation_error(request, e)

        for validated_data_generator in validated_data_generators:
            for k, param in validated_data_generator(cleaned):
                validated[k] = param

        return validated

    async def raise_on_validation_error(
        request: web.Request, exc: ValidationError
    ) -> None:
        raise web.HTTPBadRequest(
            content_type="application/json", text=json.dumps({"detail": exc.errors()})
        )

    async def wrapped(request: web.Request) -> web.StreamResponse:
        kwargs_composed = compose(request)
        kwargs_validated = await validate(request)
        kwargs = dict(**kwargs_composed, **kwargs_validated)

        resp = await handler_casted(**kwargs)

        return resp

    return wrapped


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


def _gen_validated_data_generators(meta: HandlerMeta) -> Iterator[_GenKwargsCallable]:
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
