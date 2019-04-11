import json

from aiohttp import web

from aioapi.exceptions import HTTPBadRequest

__all__ = ("validation_error_middleware",)


@web.middleware
async def validation_error_middleware(request, handler):
    try:
        resp = await handler(request)
    except HTTPBadRequest as e:
        raise web.HTTPBadRequest(
            content_type="application/json",
            text=json.dumps(
                {
                    "type": "validation_error",
                    "title": "Your request parameters didn't validate.",
                    "invalid_params": e.validation_error.errors(),
                }
            ),
        )

    return resp
