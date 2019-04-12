# aioapi

![GitHub commit merge status](https://img.shields.io/github/commit-status/Gr1N/aioapi/master/HEAD.svg?label=build%20status) [![codecov](https://codecov.io/gh/Gr1N/aioapi/branch/master/graph/badge.svg)](https://codecov.io/gh/Gr1N/aioapi) ![PyPI](https://img.shields.io/pypi/v/aioapi.svg?label=pypi%20version) ![PyPI - Downloads](https://img.shields.io/pypi/dm/aioapi.svg?label=pypi%20downloads) ![GitHub](https://img.shields.io/github/license/Gr1N/aioapi.svg)

Yet another way to build APIs using [`AIOHTTP`](https://aiohttp.readthedocs.io/) framework.

Follow [documentation](https://gr1n.github.io/aioapi/) to know what you can do with `AIOAPI`.

## Installation

```sh
$ pip install aioapi
```

## Usage

Examples of usage can be found at [`examples/`](https://github.com/Gr1N/aioapi/tree/master/example) directory.

To run example use command below:

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
