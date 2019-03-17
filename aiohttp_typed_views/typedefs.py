from typing import Generic, TypeVar

__all__ = ("PathParam",)


TVPathParam = TypeVar("TVPathParam")


class PathParam(Generic[TVPathParam]):
    __slots__ = ("_cleaned",)

    @property
    def cleaned(self) -> TVPathParam:
        return self._cleaned

    def __init__(self, cleaned: TVPathParam) -> None:
        self._cleaned = cleaned

    def __str__(self) -> str:
        return f"<PathParam({self._cleaned})>"
