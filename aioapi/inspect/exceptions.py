__all__ = (
    "HandlerInspectorError",
    "HandlerMultipleBodyError",
    "HandlerParamUnknownTypeError",
)


class HandlerInspectorError(Exception):
    __slots__ = ("_handler", "_param")

    @property
    def handler(self) -> str:
        return self._handler

    @property
    def param(self) -> str:
        return self._param

    def __init__(self, *, handler: str, param: str) -> None:
        self._handler = handler
        self._param = param

    def __str__(self) -> str:
        return repr(self)

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} handler={self._handler} param={self._param}>"
        )


class HandlerMultipleBodyError(HandlerInspectorError):
    pass


class HandlerParamUnknownTypeError(HandlerInspectorError):
    pass
