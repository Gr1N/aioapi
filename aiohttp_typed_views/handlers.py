import inspect
from dataclasses import dataclass
from http import HTTPStatus
from typing import Any, Awaitable, Callable, cast

from aiohttp import web
from aiohttp.web_routedef import _HandlerType
from pydantic import BaseModel, ValidationError, create_model

from aiohttp_typed_views.typedefs import PathParam

__all__ = ("wraps",)


@dataclass(frozen=True)
class HandlerMeta:
    name: str
    request_type: BaseModel
    request_with_path: bool = False


def wraps(handler: _HandlerType) -> _HandlerType:
    handler_casted = cast(Callable[..., Awaitable], handler)
    handler_meta = get_meta(handler_casted)

    async def wrapped(request: web.Request) -> web.StreamResponse:
        raw = {}
        if handler_meta.request_with_path:
            raw["path"] = dict(request.match_info)

        try:
            cleaned = handler_meta.request_type.parse_obj(raw)
        except ValidationError as e:
            return web.json_response(
                {"detail": e.errors()}, status=HTTPStatus.BAD_REQUEST
            )

        kwargs = {}
        if handler_meta.request_with_path:
            for k, v in cleaned.path:  # type: ignore
                kwargs[k] = PathParam(v)

        resp = await handler_casted(**kwargs)

        return resp

    return wrapped


def get_meta(handler: Callable[..., Awaitable]) -> HandlerMeta:
    handler_name = f"{handler.__module__}.{handler.__name__}"

    path_mapping = {}

    signature = inspect.signature(handler)
    for param in signature.parameters.values():
        param_name = param.name
        param_type = param.annotation

        if param_of(type_=param_type, is_=PathParam):
            path_mapping[param_name] = param_inner_type(param_type)
        else:
            raise RuntimeError(f"Bad param: handler{handler_name}; param={param_name}")

    request_mapping = {}
    if path_mapping:
        request_mapping["path"] = (
            create_model(  # type: ignore
                "Path", **{k: (v, ...) for k, v in path_mapping.items()}
            ),
            ...,
        )

    request_type = create_model("Request", **request_mapping)  # type: ignore

    return HandlerMeta(
        name=handler_name,
        request_type=request_type,
        request_with_path="path" in request_mapping,
    )


def param_of(*, type_, is_) -> bool:
    return getattr(type_, "__origin__", type_) is is_


def param_inner_type(type_) -> Any:
    return getattr(type_, "__args__", (Any,))[0]
