# aioapi

[![Build Status](https://github.com/Gr1N/aioapi/workflows/default/badge.svg)](https://github.com/Gr1N/aioapi/actions?query=workflow%3Adefault) [![codecov](https://codecov.io/gh/Gr1N/aioapi/branch/master/graph/badge.svg)](https://codecov.io/gh/Gr1N/aioapi) ![PyPI](https://img.shields.io/pypi/v/aioapi.svg?label=pypi%20version) ![PyPI - Downloads](https://img.shields.io/pypi/dm/aioapi.svg?label=pypi%20downloads) ![GitHub](https://img.shields.io/github/license/Gr1N/aioapi.svg)

Yet another way to build APIs using [`AIOHTTP`](https://aiohttp.readthedocs.io/) framework.

Follow [documentation](https://gr1n.github.io/aioapi/) to know what you can do with `AIOAPI`.

## Installation

```sh
$ pip install aioapi
```

## Usage & Examples

Below you can find a simple, but powerful example of `AIOAPI` library usage:

```python
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

And there are also more examples of usage at [`examples/`](https://github.com/Gr1N/aioapi/tree/master/example) directory.

To run them use command below:

```sh
$ make example
```

## Contributing

To work on the `AIOAPI` codebase, you'll want to clone the project locally and install the required dependencies via [poetry](https://poetry.eustace.io):

```sh
$ git clone git@github.com:Gr1N/aioapi.git
$ make install
```

To run tests and linters use command below:

```sh
$ make lint && make test
```

If you want to run only tests or linters you can explicitly specify what you want to run, e.g.:

```sh
$ make lint-black
```

## Milestones

If you're interesting in project's future you can find milestones and plans at [projects](https://github.com/Gr1N/aioapi/projects) page.

## License

`AIOAPI` is licensed under the MIT license. See the license file for details.
