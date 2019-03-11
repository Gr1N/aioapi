# aiohttp-typed-views

Typed class based views for [`aiohttp`](https://aiohttp.readthedocs.io/) framework.

## Installation

```sh
$ pip install aiohttp-typed-views
```

## Usage

Examples of usage can be found at `examples` directory.

## Contributing

To work on the `aiohttp-typed-views` codebase, you'll want to clone the project locally and install the required dependencies via [poetry](https://poetry.eustace.io):

```sh
$ git clone git@github.com:Gr1N/aiohttp-typed-views.git
$ poetry install
```

To run tests and linters use command below:

```sh
$ poetry run tox
```

If you want to run only tests or linters you can explicitly specify which test environment you want to run, e.g.:

```sh
$ poetry run tox -e py37-tests
```

## TODO

### 0.2.0

* [ ] path parameters
* [ ] query parameters
* [ ] request body

### 0.3.0

* [ ] cookie parameters
* [ ] header parameters
* [ ] response body

### 0.4.0

* [ ] OpenAPI

### 0.5.0

* [ ] request form data
* [ ] request files

## License

`aiohttp-typed-views` is licensed under the MIT license. See the license file for details.
