import json
from dataclasses import dataclass
from typing import Awaitable, Callable, Dict, Iterator, Tuple, Union, cast

from aiohttp import hdrs, web
from aiohttp.abc import AbstractView
from aiohttp.web_routedef import _HandlerType, _SimpleHandler
from pydantic import BaseModel, ValidationError

from aioapi.exceptions import HTTPBadRequest
from aioapi.inspect.entities import HandlerMeta
from aioapi.inspect.inspector import HandlerInspector, param_of
from aioapi.typedefs import Body, PathParam, QueryParam

__all__ = ("wraps", "wraps_simple", "wraps_method")

_HandlerCallable = Callable[..., Awaitable]
_HandlerParams = Union[Body, PathParam, QueryParam, web.Application, web.Request]
_HandlerKwargs = Dict[str, _HandlerParams]

_GenRawDataResult = Tuple[str, dict]
_GenRawDataCallable = Callable[[web.Request], Awaitable[_GenRawDataResult]]

_GenKwargsResult = Iterator[Tuple[str, _HandlerParams]]
_GenKwargsCallable = Callable[[HandlerMeta, BaseModel], _GenKwargsResult]


@dataclass(frozen=True)
class DataGenerators:
    raw: Tuple[_GenRawDataCallable, ...]
    kwargs: Tuple[_GenKwargsCallable, ...]


def wraps(handler: _HandlerType) -> _HandlerType:
    try:
        issubclass(handler, AbstractView)  # type: ignore
    except TypeError:
        return wraps_simple(cast(_SimpleHandler, handler))

    for method in hdrs.METH_ALL:
        method = method.lower()

        handler_callable = getattr(handler, method, None)
        if handler_callable is None:
            continue

        handler_name = (
            f"{handler.__module__}.{handler.__name__}"  # type: ignore
            f".{handler_callable.__name__}"
        )
        setattr(
            handler,
            method,
            wraps_method(handler=handler_callable, handler_name=handler_name),
        )

    return handler


def wraps_simple(handler: _SimpleHandler) -> _SimpleHandler:
    handler_casted = cast(_HandlerCallable, handler)
    handler_meta = HandlerInspector(handler=handler_casted)()
    data_generators = _get_data_generators(handler_meta)

    async def wrapped(request: web.Request) -> web.StreamResponse:
        kwargs = await _handle_kwargs(handler_meta, data_generators, request)
        resp = await handler_casted(**kwargs)

        return resp

    return wrapped


def wraps_method(*, handler: _HandlerCallable, handler_name: str):
    handler_meta = HandlerInspector(handler=handler, handler_name=handler_name)()
    data_generators = _get_data_generators(handler_meta)

    async def wrapped(self) -> web.StreamResponse:
        kwargs = await _handle_kwargs(handler_meta, data_generators, self.request)
        resp = await handler(self, **kwargs)

        return resp

    return wrapped


async def _handle_kwargs(
    meta: HandlerMeta, data_generators: DataGenerators, request: web.Request
) -> _HandlerKwargs:
    kwargs_composed = _compose_kwargs(meta, request)
    kwargs_validated = await _validate_kwargs(meta, data_generators, request)

    return dict(**kwargs_composed, **kwargs_validated)


def _compose_kwargs(meta: HandlerMeta, request: web.Request) -> _HandlerKwargs:
    composed: _HandlerKwargs = {}
    if meta.components_mapping is None:
        return composed

    for k, type_ in meta.components_mapping.items():
        if param_of(type_=type_, is_=web.Application):
            composed[k] = request.app
        elif param_of(type_=type_, is_=web.Request):  # pragma: no branch
            composed[k] = request

    return composed


async def _validate_kwargs(
    meta: HandlerMeta, data_generators: DataGenerators, request: web.Request
) -> _HandlerKwargs:
    validated: _HandlerKwargs = {}
    if meta.request_type is None:
        return validated

    raw = {}
    for raw_data_generator in data_generators.raw:
        k, raw_data = await raw_data_generator(request)
        raw[k] = raw_data

    try:
        cleaned = cast(BaseModel, meta.request_type).parse_obj(raw)
    except ValidationError as e:
        raise HTTPBadRequest(validation_error=e) from e

    for kwargs_data_generator in data_generators.kwargs:
        for k, param in kwargs_data_generator(meta, cleaned):
            validated[k] = param

    return validated


def _get_data_generators(meta: HandlerMeta) -> DataGenerators:
    return DataGenerators(
        raw=tuple(_gen_raw_data_generators(meta)),
        kwargs=tuple(_gen_kwargs_data_generators(meta)),
    )


def _gen_raw_data_generators(meta: HandlerMeta) -> Iterator[_GenRawDataCallable]:
    if meta.request_body_pair:
        yield _gen_body_raw_data

    if meta.request_path_mapping:
        yield _gen_path_raw_data

    if meta.request_query_mapping:
        yield _gen_query_raw_data


async def _gen_body_raw_data(request: web.Request) -> _GenRawDataResult:
    try:
        raw = await request.json()
    except json.JSONDecodeError:
        raw = {}

    return "body", raw


async def _gen_path_raw_data(request: web.Request) -> _GenRawDataResult:
    return "path", dict(request.match_info)


async def _gen_query_raw_data(request: web.Request) -> _GenRawDataResult:
    return "query", dict(request.query)


def _gen_kwargs_data_generators(meta: HandlerMeta) -> Iterator[_GenKwargsCallable]:
    if meta.request_body_pair:
        yield _gen_body_kwargs

    if meta.request_path_mapping:
        yield _gen_path_kwargs

    if meta.request_query_mapping:
        yield _gen_query_kwargs


def _gen_body_kwargs(meta: HandlerMeta, cleaned: BaseModel) -> _GenKwargsResult:
    k, _ = cast(tuple, meta.request_body_pair)
    yield k, Body(cleaned.body)  # type: ignore


def _gen_path_kwargs(_meta: HandlerMeta, cleaned: BaseModel) -> _GenKwargsResult:
    for k, v in cleaned.path:  # type: ignore
        yield k, PathParam(v)


def _gen_query_kwargs(_meta: HandlerMeta, cleaned: BaseModel) -> _GenKwargsResult:
    for k, v in cleaned.query:  # type: ignore
        yield k, QueryParam(v)
