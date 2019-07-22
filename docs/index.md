# AIOAPI

[![Build Status](https://cloud.drone.io/api/badges/Gr1N/aioapi/status.svg)](https://cloud.drone.io/Gr1N/aioapi) [![codecov](https://codecov.io/gh/Gr1N/aioapi/branch/master/graph/badge.svg)](https://codecov.io/gh/Gr1N/aioapi) ![PyPI](https://img.shields.io/pypi/v/aioapi.svg?label=pypi%20version) ![PyPI - Downloads](https://img.shields.io/pypi/dm/aioapi.svg?label=pypi%20downloads) ![GitHub](https://img.shields.io/github/license/Gr1N/aioapi.svg)

`AIOAPI` is a library for building APIs with [`AIOHTTP`](https://aiohttp.readthedocs.io/) framework and Python 3.7+ based on standard Python type hints.

## Install

Just:

```bash
$ pip install aioapi
```

## Requirements

`AIOAPI` depends on [`AIOHTTP`](https://aiohttp.readthedocs.io/) framework and tries to extend the view layer in the right way, also `AIOAPI` depends on [`pydantic`](https://pydantic-docs.helpmanual.io/) — a great data validation library.

## At a glance

Look at simple application below and pay attention to the highlighted lines to see the power of `AIOAPI`:

```python hl_lines="24 31"
from http import HTTPStatus
from uuid import UUID

import aioapi as api
from aioapi import Body, PathParam
from aiohttp import web
from pydantic import BaseModel


class Database:
    async def get_user(self, *, user_id):
        ...

    async def create_user(self, *, user_id, name, age):
        ...


class User(BaseModel):
    user_id: UUID
    name: string
    age: int = 42


async def get_user(app: web.Application, user_id: PathParam[UUID]):
    user = await app["db"].get_user(user_id=user_id)

    return web.json_response(
        {"user_id": user.user_id, "name": user.name, "age": user.age}
    )

async def create_user(app: web.Application, body: Body[User])
    user = body.cleaned
    await app["db"].create_user(
        user_id=user.user_id, name=user.name, age=user.age
    )

    return web.Response(status=HTTPStatus.CREATED)


def main():
    app = web.Application()

    app["db"] = Database()
    app.add_routes([
        api.post("/users", create_user),
        api.get("/users/{user_id}", get_user),
    ])

    web.run_app(app)


if __name__ == "__main__":
    main()
```

That simple example shows you how `AIOAPI` can help you to simplify your daily routine with data serialization and validation in APIs. As you can see you need just to define the right types and `AIOAPI` will do all other job for you.

Looks interesting for you? Go ahead and explore documentation, `AIOAPI` can surprise you!
