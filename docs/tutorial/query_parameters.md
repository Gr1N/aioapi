# Query Parameters

You can declare query parameters and their types, using standard Python type annotations:

```python hl_lines="7"
import aioapi as api
from aioapi import QueryParam
from aioapi.middlewares import validation_error_middleware
from aiohttp import web


async def hello_query(name: QueryParam[str]):
    return web.json_response({"name": name.cleaned})


def main():
    app = web.Application()

    app.add_routes([api.get("/hello_query", hello_query)])
    app.middlewares.append(validation_error_middleware)

    web.run_app(app)


if __name__ == "__main__":
    main()
```

Query parameters can have default values:

```python hl_lines="3"
async def hello_query(
    name: QueryParam[str],
    age: QueryParam[int] = QueryParam(42),
):
    return web.json_response({
        "name": name.cleaned,
        "age": age.cleaned,
    })
```

If you run this example and send a request to `/hello_query?name=batman` route you will see:

```bash
$ http :8080/hello_query?name=batman
HTTP/1.1 200 OK
Content-Length: 30
Content-Type: application/json; charset=utf-8
Date: Fri, 12 Apr 2019 19:29:18 GMT
Server: Python/3.7 aiohttp/3.5.4

{
    "age": 42,
    "name": "batman"
}
```

But if you send a request to `/hello_query` route you will see an error:

```bash
$ http :8080/hello_query
HTTP/1.1 400 Bad Request
Content-Length: 185
Content-Type: application/json; charset=utf-8
Date: Fri, 12 Apr 2019 19:33:45 GMT
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
