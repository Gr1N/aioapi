# Request Body

You can declare a request body and its type, using standard Python type annotations.

The request body, as well as query parameters, can be defined with a default value.

To declare body type use `pydantic` models.

And you can always combine and use path and query parameters, and request body in one view.

```python hl_lines="5 8 9 10 13"
import aioapi as api
from aioapi import Body, PathParam
from aioapi.middlewares import validation_error_middleware
from aiohttp import web
from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int = 42


async def hello_body(user_id: PathParam[int], body: Body[User]):
    user = body.cleaned
    return web.json_response(
        {"id": user_id.cleaned, "name": user.name, "age": user.age}
    )


def main():
    app = web.Application()

    app.add_routes([api.post("/hello/{user_id}", hello_body)])
    app.middlewares.append(validation_error_middleware)

    web.run_app(app)


if __name__ == "__main__":
    main()
```

If you run this example and send a request to `/hello/42` route you will see:

```bash
$ http :8080/hello/42 name=batman
HTTP/1.1 200 OK
Content-Length: 39
Content-Type: application/json; charset=utf-8
Date: Fri, 12 Apr 2019 19:56:47 GMT
Server: Python/3.7 aiohttp/3.5.4

{
    "age": 42,
    "id": 42,
    "name": "batman"
}
```

But if you send a request to `/hello/batman` route you will see an error:

```bash
$ http :8080/hello/batman age=random
HTTP/1.1 400 Bad Request
Content-Length: 378
Content-Type: application/json; charset=utf-8
Date: Fri, 12 Apr 2019 19:57:49 GMT
Server: Python/3.7 aiohttp/3.5.4

{
    "invalid_params": [
        {
            "loc": [
                "body",
                "name"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        },
        {
            "loc": [
                "body",
                "age"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        },
        {
            "loc": [
                "path",
                "user_id"
            ],
            "msg": "value is not a valid integer",
            "type": "type_error.integer"
        }
    ],
    "title": "Your request parameters didn't validate.",
    "type": "validation_error"
}
```
