# Path Parameters

You can declare path parameters and their types, using standard Python type annotations:

```python hl_lines="7"
import aioapi as api
from aioapi import PathParam
from aioapi.middlewares import validation_error_middleware
from aiohttp import web


async def hello_path(number: PathParam[int]):
    return web.json_response({"hello", number.cleaned})


def main():
    app = web.Application()

    app.add_routes([api.get("/hello/{number}", hello_path)])
    app.middlewares.append(validation_error_middleware)

    web.run_app(app)


if __name__ == "__main__":
    main()
```

If you run this example and send a request to `/hello/42` route you will see:

```bash
$ http :8080/hello/42
HTTP/1.1 200 OK
Content-Length: 13
Content-Type: application/json; charset=utf-8
Date: Fri, 12 Apr 2019 19:18:54 GMT
Server: Python/3.7 aiohttp/3.5.4

{
    "hello": 42
}
```

But if you send a request to `/hello/batman` route you will see an error:

```bash
$ http :8080/hello/batman
HTTP/1.1 400 Bad Request
Content-Length: 199
Content-Type: application/json; charset=utf-8
Date: Fri, 12 Apr 2019 19:20:44 GMT
Server: Python/3.7 aiohttp/3.5.4

{
    "invalid_params": [
        {
            "loc": [
                "path",
                "number"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ],
    "title": "Your request parameters didn't validate.",
    "type": "validation_error"
}
```
