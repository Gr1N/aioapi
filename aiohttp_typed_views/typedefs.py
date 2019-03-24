from typing import Generic, TypeVar

__all__ = ("Body", "PathParam", "QueryParam")


TVBody = TypeVar("TVBody")
TVPathParam = TypeVar("TVPathParam")
TVQueryParam = TypeVar("TVQueryParam")


class Body(Generic[TVBody]):
    __slots__ = ("_cleaned",)

    @property
    def cleaned(self) -> TVBody:
        return self._cleaned

    def __init__(self, cleaned: TVBody) -> None:
        self._cleaned = cleaned

    def __str__(self) -> str:
        return f"<Body({self._cleaned})>"


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
