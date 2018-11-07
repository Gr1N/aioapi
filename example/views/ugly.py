import json
from http import HTTPStatus
from uuid import UUID

from aiohttp import web
from pydantic import ValidationError

from example.schemas import User

__all__ = ("UglyView",)


class UglyView(web.View):
    async def post(self):
        try:
            body = await self.request.json()
        except json.JSONDecodeError:
            body = {}

        try:
            user = User.parse_obj(body)
        except ValidationError as e:
            return web.json_response(e.errors(), status=HTTPStatus.BAD_REQUEST)

        try:
            trace_id = UUID(self.request.query.get("trace_id"))
        except (TypeError, ValueError):
            return web.json_response(
                "invalid `trace_id`", status=HTTPStatus.BAD_REQUEST
            )

        return web.json_response(
            {
                "_hello": "handsome",
                "first_name": user.first_name,
                "last_name": user.last_name,
                "trace_id": str(trace_id),
            }
        )
