# Components

`AIOAPI` supports components which you can use in your views, using standard Python type annotations.

Supported components:

* `aiohttp.web.Request`
* `aiohttp.web.Application`

Below you can find a real example of request and application components usage:

```python hl_lines="5"
import aioapi as api
from aiohttp import web


async def hello_components(request: web.Request, app: web.Application):
    return web.Response()


def main():
    app = web.Application()

    app.add_routes([api.get("/hello_components", hello_components)])

    web.run_app(app)


if __name__ == "__main__":
    main()
```
