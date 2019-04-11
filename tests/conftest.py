import pytest
from aiohttp import web

from aioapi.middlewares import validation_error_middleware


@pytest.fixture
def client_for(aiohttp_client):
    async def _client_for(*, routes):
        app = web.Application()
        app.add_routes(routes)
        app.middlewares.append(validation_error_middleware)

        return await aiohttp_client(app)

    return _client_for
