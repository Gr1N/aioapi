from typing import Generic, TypeVar

__all__ = ("Body", "QueryParam")


TB = TypeVar("TB")
TQ = TypeVar("TQ")


class Body(Generic[TB]):
    __slots__ = ("_value",)

    @property
    def value(self) -> TB:
        return self._value

    def __init__(self, value: TB) -> None:
        self._value = value

    def __str__(self) -> str:
        return f"<Body({self._value})>"


class QueryParam(Generic[TQ]):
    __slots__ = ("_value",)

    @property
    def value(self) -> TQ:
        return self._value

    def __init__(self, value: TQ) -> None:
        self._value = value

    def __str__(self) -> str:
        return f"<QueryParam({self._value})>"
