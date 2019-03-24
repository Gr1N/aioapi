__all__ = (
    "HandlerInspectorError",
    "HandlerMultipleBodyError",
    "HandlerParamUnknownTypeError",
)


class HandlerInspectorError(Exception):
    __slots__ = ("_handler", "_param")

    def __init__(self, *, handler: str, param: str) -> None:
        self._handler = handler
        self._param = param


class HandlerMultipleBodyError(HandlerInspectorError):
    pass


class HandlerParamUnknownTypeError(HandlerInspectorError):
    pass
