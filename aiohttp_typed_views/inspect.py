import inspect
from dataclasses import dataclass
from typing import Any, Awaitable, Callable

from pydantic import BaseModel, Required, create_model

from aiohttp_typed_views.typedefs import PathParam, QueryParam

__all__ = ("HandlerMeta", "HandlerInspector", "HandlerInspectorError")


@dataclass(frozen=True)
class HandlerMeta:
    name: str
    request_type: BaseModel
    request_with_path: bool = False
    request_with_query: bool = False


class HandlerInspector:
    __slots__ = ("_handler", "_handler_name")

    def __init__(self, handler: Callable[..., Awaitable]) -> None:
        self._handler = handler
        self._handler_name = f"{handler.__module__}.{handler.__name__}"

    def __call__(self) -> HandlerMeta:
        path_mapping = {}
        query_mapping = {}

        signature = inspect.signature(self._handler)
        for param in signature.parameters.values():
            param_name = param.name
            param_type = param.annotation

            if param_of(type_=param_type, is_=PathParam):
                path_mapping[param_name] = param_inner_type(param_type), Required
            elif param_of(type_=param_type, is_=QueryParam):
                query_mapping[param_name] = (
                    param_inner_type(param_type),
                    param_default(param.default),
                )
            else:
                raise HandlerInspectorError(
                    f"Bad param: handler={self._handler_name}; param={param_name}"
                )

        request_mapping = {}
        for k, mapping in (("path", path_mapping), ("query", query_mapping)):
            if not mapping:
                continue

            request_mapping[k] = (
                create_model(  # type: ignore
                    k.title(), **{k: v for k, v in mapping.items()}
                ),
                Required,
            )

        request_type = create_model("Request", **request_mapping)  # type: ignore

        return HandlerMeta(
            name=self._handler_name,
            request_type=request_type,
            request_with_path="path" in request_mapping,
            request_with_query="query" in request_mapping,
        )


class HandlerInspectorError(Exception):
    pass


def param_of(*, type_, is_) -> bool:
    return getattr(type_, "__origin__", type_) is is_


def param_inner_type(type_) -> Any:
    return getattr(type_, "__args__", (Any,))[0]


def param_default(default):
    if default == inspect.Signature.empty:
        return Required

    return getattr(default, "cleaned", default)
