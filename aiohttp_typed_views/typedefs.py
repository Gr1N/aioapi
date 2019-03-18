from typing import Generic, TypeVar

__all__ = ("PathParam", "QueryParam")


TVPathParam = TypeVar("TVPathParam")
TVQueryParam = TypeVar("TVQueryParam")


class PathParam(Generic[TVPathParam]):
    __slots__ = ("_cleaned",)

    @property
    def cleaned(self) -> TVPathParam:
        return self._cleaned

    def __init__(self, cleaned: TVPathParam) -> None:
        self._cleaned = cleaned

    def __str__(self) -> str:
        return f"<PathParam({self._cleaned})>"


class QueryParam(Generic[TVQueryParam]):
    __slots__ = ("_cleaned",)

    @property
    def cleaned(self) -> TVQueryParam:
        return self._cleaned

    def __init__(self, cleaned: TVQueryParam) -> None:
        self._cleaned = cleaned

    def __str__(self) -> str:
        return f"<QueryParam({self._cleaned})>"
