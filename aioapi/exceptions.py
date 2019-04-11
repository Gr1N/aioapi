from aiohttp import web
from pydantic import ValidationError

__all__ = ("HTTPBadRequest",)


class HTTPBadRequest(web.HTTPBadRequest):
    __slots__ = ("_validation_error",)

    @property
    def validation_error(self) -> ValidationError:
        return self._validation_error

    def __init__(self, *, validation_error: ValidationError, **kwargs) -> None:
        self._validation_error = validation_error
        super().__init__(**kwargs)
