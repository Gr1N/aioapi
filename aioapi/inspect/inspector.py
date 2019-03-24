import inspect
from typing import Any, Awaitable, Callable, Tuple

from pydantic import Required, create_model

from aioapi.inspect.entities import HandlerMeta
from aioapi.inspect.exceptions import (
    HandlerMultipleBodyError,
    HandlerParamUnknownTypeError,
)
from aioapi.typedefs import Body, PathParam, QueryParam

__all__ = ("HandlerInspector",)

NOT_INITIALIZED = object()


class HandlerInspector:
    __slots__ = ("_handler", "_handler_name")

    def __init__(self, handler: Callable[..., Awaitable]) -> None:
        self._handler = handler
        self._handler_name = f"{handler.__module__}.{handler.__name__}"

    def __call__(self) -> HandlerMeta:
        body_pair = None
        path_mapping = {}
        query_mapping = {}

        signature = inspect.signature(self._handler)
        for param in signature.parameters.values():
            param_name = param.name
            param_type = param.annotation

            if param_of(type_=param_type, is_=Body):
                # We allow only one parameter of body type, so if there are more
                # parameters of body type we will raise a corresponding error.
                if body_pair is not None:
                    raise HandlerMultipleBodyError(
                        handler=self._handler_name, param=param_name
                    )

                body_pair = (
                    param_name,
                    inspect_param_type(param_type, inspect_default=param.default),
                )
            elif param_of(type_=param_type, is_=PathParam):
                path_mapping[param_name] = inspect_param_type(param_type)
            elif param_of(type_=param_type, is_=QueryParam):
                query_mapping[param_name] = inspect_param_type(
                    param_type, inspect_default=param.default
                )
            else:
                raise HandlerParamUnknownTypeError(
                    handler=self._handler_name, param=param_name
                )

        request_mapping = {}
        if body_pair:
            _, body_type = body_pair
            request_mapping["body"] = body_type

        for k, mapping in (("path", path_mapping), ("query", query_mapping)):
            if not mapping:
                continue

            request_mapping[k] = (
                create_model(  # type: ignore
                    k.title(), **{k: v for k, v in mapping.items()}
                ),
                Required,
            )

        request_type = (
            create_model("Request", **request_mapping)  # type: ignore
            if request_mapping
            else None
        )

        return HandlerMeta(
            name=self._handler_name,
            request_type=request_type,
            request_body_pair=body_pair,
            request_path_mapping=path_mapping or None,
            request_query_mapping=query_mapping or None,
        )


def param_of(*, type_, is_) -> bool:
    return getattr(type_, "__origin__", type_) is is_


def inspect_param_type(
    type_, *, inspect_default: Any = NOT_INITIALIZED
) -> Tuple[Any, Any]:
    return (
        inspect_param_inner_type(type_),
        (
            inspect_param_default(inspect_default)
            if inspect_default is not NOT_INITIALIZED
            else Required
        ),
    )


def inspect_param_inner_type(type_) -> Any:
    return getattr(type_, "__args__", (Any,))[0]


def inspect_param_default(default: Any) -> Any:
    if default == inspect.Signature.empty:
        return Required

    return getattr(default, "cleaned", default)
