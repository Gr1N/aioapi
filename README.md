# aioapi

Yet another way to build APIs using [`AIOHTTP`](https://aiohttp.readthedocs.io/) framework.

## Installation

```sh
$ pip install aioapi
```

## Usage

Examples of usage can be found at `examples` directory.

To run example use command below:

```sh
$ make example
```

## Contributing

To work on the `aioapi` codebase, you'll want to clone the project locally and install the required dependencies via [poetry](https://poetry.eustace.io):

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

`aioapi` is licensed under the MIT license. See the license file for details.
