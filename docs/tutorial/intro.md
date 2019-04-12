# Intro

This tutorial shows you how to use `AIOAPI` with all its features, step by step.

## Install AIOAPI

Install `AIOAPI`:

```bash
$ pip install aioapi
```

## First Steps

Create simple `AIOHTTP` application, during tutorial we will extend it step by step:

```python
import aioapi as api
from aioapi.middlewares import validation_error_middleware
from aiohttp import web


async def hello_aioapi():
    return web.json_response({"hello": "AIOAPI"})


def main():
    app = web.Application()

    app.add_routes([api.get("/", hello_aioapi)])
    app.middlewares.append(validation_error_middleware)

    web.run_app(app)


if __name__ == "__main__":
    main()
```

Copy that to a file `main.py` and run the live server:

```bash
$ python main.py
```

Open browser at [http://127.0.0.1:8080](http://127.0.0.1:8080) or use command line tool like [cURL](https://curl.haxx.se/) or [HTTPie](https://httpie.org/) to check that server is up and running:

```bash
$ http :8080
HTTP/1.1 200 OK
Content-Length: 19
Content-Type: application/json; charset=utf-8
Date: Fri, 12 Apr 2019 17:44:31 GMT
Server: Python/3.7 aiohttp/3.5.4

{
    "hello": "AIOAPI"
}
```

## Examples

You can also skip the tutorial and jump into [`examples/`](https://github.com/Gr1N/aioapi/tree/master/example) directory where you can find an example application which shows all power of `AIOAPI` library.
