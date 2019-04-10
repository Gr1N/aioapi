import pytest
from aiohttp import web


@pytest.fixture
def client_for(aiohttp_client):
    async def _client_for(*, routes):
        app = web.Application()
        app.add_routes(routes)

        return await aiohttp_client(app)

    return _client_for
