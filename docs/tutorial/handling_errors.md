# Handling Errors

`AIOAPI` by default returns empty `400 Bad Request` response in case of any validation error.

If you run example below:

```python
import aioapi as api
from aioapi import QueryParam
from aiohttp import web


async def hello_errors(name: QueryParam[str]):
    return web.Response()


def main():
    app = web.Application()

    app.add_routes([api.get("/hello_errors", hello_errors)])

    web.run_app(app)


if __name__ == "__main__":
    main()
```

And send request to `/hello_errors` route you will see:

```bash
$ http :8080/hello_errors
HTTP/1.1 400 Bad Request
Content-Length: 16
Content-Type: text/plain; charset=utf-8
Date: Fri, 12 Apr 2019 20:24:50 GMT
Server: Python/3.7 aiohttp/3.5.4

400: Bad Request
```

To get more fancy `400 Bad Request` response you can use `validation_error_middleware` middleware:

```python hl_lines="3 15"
import aioapi as api
from aioapi import QueryParam
from aioapi.middlewares import validation_error_middleware
from aiohttp import web


async def hello_errors(name: QueryParam[str]):
    return web.Response()


def main():
    app = web.Application()

    app.add_routes([api.get("/hello_errors", hello_errors)])
    app.middlewares.append(validation_error_middleware)

    web.run_app(app)


if __name__ == "__main__":
    main()
```

If you send a request to `/hello_errors` route you will see an error:

```bash
$ http :8080/hello_errors
HTTP/1.1 400 Bad Request
Content-Length: 185
Content-Type: application/json; charset=utf-8
Date: Fri, 12 Apr 2019 20:31:49 GMT
Server: Python/3.7 aiohttp/3.5.4

{
    "invalid_params": [
        {
            "loc": [
                "query",
                "name"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ],
    "title": "Your request parameters didn't validate.",
    "type": "validation_error"
}
```

And also you can write your own middleware to handle validation errors:

```python hl_lines="13 14 15 16 17 18 19 20 21 22 23 30"
import json

import aioapi as api
from aioapi import QueryParam
from aioapi.exceptions import HTTPBadRequest
from aiohttp import web


async def hello_errors(name: QueryParam[str]):
    return web.Response()


@web.middleware
async def custom_error_middleware(request, handler):
    try:
        resp = await handler(request)
    except HTTPBadRequest as e:
        raise web.HTTPBadRequest(
            content_type="application/json",
            text=json.dumps(e.validation_error.errors()),
        )

    return resp


def main():
    app = web.Application()

    app.add_routes([api.get("/hello_errors", hello_errors)])
    app.middlewares.append(custom_error_middleware)

    web.run_app(app)


if __name__ == "__main__":
    main()
```

If you send a request to `/hello_errors` route you will see an error:

```bash
$ http :8080/hello_errors
HTTP/1.1 400 Bad Request
Content-Length: 84
Content-Type: application/json; charset=utf-8
Date: Fri, 12 Apr 2019 20:34:56 GMT
Server: Python/3.7 aiohttp/3.5.4

[
    {
        "loc": [
            "query",
            "name"
        ],
        "msg": "field required",
        "type": "value_error.missing"
    }
]
```
