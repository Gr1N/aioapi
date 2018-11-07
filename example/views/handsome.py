from uuid import UUID

from aiohttp import web

from aiohttp_typed_views import Body, QueryParam, TypeView
from example.schemas import User

__all__ = ("HandsomeView",)


class HandsomeView(TypeView):
    async def post(self, body: Body[User], trace_id: QueryParam[UUID]):
        return web.json_response(
            {
                "_hello": "handsome",
                "first_name": body.value.first_name,
                "last_name": body.value.last_name,
                "trace_id": str(trace_id.value),
            }
        )
