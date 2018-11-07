# aiohttp-typed-views [![Build Status](https://travis-ci.org/Gr1N/aiohttp-typed-views.svg?branch=master)](https://travis-ci.org/Gr1N/aiohttp-typed-views) [![codecov](https://codecov.io/gh/Gr1N/aiohttp-typed-views/branch/master/graph/badge.svg)](https://codecov.io/gh/Gr1N/aiohttp-typed-views) [![Updates](https://pyup.io/repos/github/Gr1N/aiohttp-typed-views/shield.svg)](https://pyup.io/repos/github/Gr1N/aiohttp-typed-views/) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

Typed class based views for [`aiohttp`](https://aiohttp.readthedocs.io/) framework.

## Installation

    $ pip install aiohttp-typed-views

## Usage

## Contributing

To work on the `aiohttp-typed-views` codebase, you'll want to clone the project locally and install the required dependencies via [poetry](https://poetry.eustace.io):

    $ git clone git@github.com:Gr1N/aiohttp-typed-views.git
    $ poetry install

To run tests and linters use command below:

    $ poetry run tox

If you want to run only tests or linters you can explicitly specify which test environment you want to run, e.g.:

    $ poetry run tox -e py37-tests

## License

`aiohttp-typed-views` is licensed under the MIT license. See the license file for details.
