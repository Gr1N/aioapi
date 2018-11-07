import inspect
import json
from dataclasses import dataclass
from http import HTTPStatus
from textwrap import dedent
from typing import Any, Awaitable, Callable, Dict, Optional, Tuple, Union

from aiohttp import hdrs, web
from pydantic import BaseModel, ValidationError, create_model

from aiohttp_typed_views.types import Body, QueryParam

__all__ = ("TypeView",)


@dataclass
class TypeViewMeta:
    name: str
    description: Optional[str]
    body_mapping: dict
    query_mapping: dict
    request_type: BaseModel


class TypeViewInspector:
    __slots__ = ("_method", "_method_name")

    def __init__(self, method: Callable[..., Awaitable]) -> None:
        self._method = method
        self._method_name = f"{self._method.__module__}.{self._method.__name__}"

    def get_meta(self) -> TypeViewMeta:
        signature = inspect.signature(self._method)

        description = self._method.__doc__
        if description is not None:
            description = dedent(description).strip(" \r\n\t")

        body_mapping, query_mapping = self.get_args(signature)

        request_mapping = {}
        if body_mapping:
            request_mapping["body"] = (tuple(body_mapping.values())[0], ...)
        if query_mapping:
            request_mapping["query"] = (
                create_model(
                    "Query", **{k: (v, ...) for k, v in query_mapping.items()}
                ),
                ...,
            )

        request_type = create_model("Request", **request_mapping)

        return TypeViewMeta(
            name=self._method_name,
            description=description,
            body_mapping=body_mapping,
            query_mapping=query_mapping,
            request_type=request_type,
        )

    def get_args(self, signature: inspect.Signature) -> Tuple[dict, dict]:
        params_to_skip = {"self", "args", "kwargs"}

        body = {}
        query = {}

        for param in signature.parameters.values():
            param_name = param.name
            param_type = param.annotation
            if param_type is inspect.Signature.empty and param_name in params_to_skip:
                continue

            if self._arg_is(param_type, Body):
                body[param_name] = self._get_arg_inner_type(param_type)
            elif self._arg_is(param_type, QueryParam):
                query[param_name] = self._get_arg_inner_type(param_type)
            else:
                raise RuntimeError(
                    f"Bad param: method={self._method_name}; param={param_name}"
                )

        return body, query

    def _arg_is(self, type_, klass) -> bool:
        return getattr(type_, "__origin__", type_) is klass

    def _get_arg_inner_type(self, type_) -> Any:
        return getattr(type_, "__args__", (Any,))[0]

    def _create_model(self, name: str, types: dict) -> Optional[BaseModel]:
        return (
            create_model(name, **{k: (v, ...) for k, v in types.items()})
            if types
            else None
        )


class TypeView(web.View):
    async def _iter(self) -> web.StreamResponse:
        if self.request.method not in hdrs.METH_ALL:
            self._raise_allowed_methods()

        method = getattr(self, self.request.method.lower(), None)
        if method is None:
            self._raise_allowed_methods()

        # inspect method signature
        inspector = TypeViewInspector(method)
        meta = inspector.get_meta()

        # prepare data for validation
        raw = {}
        if meta.body_mapping:
            try:
                raw["body"] = await self.request.json()
            except json.JSONDecodeError:
                raw["body"] = {}
        if meta.query_mapping:
            raw["query"] = dict(self.request.query)

        # run validation
        try:
            cleaned = meta.request_type(**raw)
        except ValidationError as e:
            return web.json_response(e.errors(), status=HTTPStatus.BAD_REQUEST)

        # prepare method arguments
        args: Dict[str, Union[Body, QueryParam]] = {}
        if meta.body_mapping:
            args[tuple(meta.body_mapping.keys())[0]] = Body(cleaned.body)
        if meta.query_mapping:
            for k, v in cleaned.query:
                args[k] = QueryParam(v)

        # run method with cleaned args
        resp = await method(**args)

        return resp
