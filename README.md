<!-- Banner -->
![alt Banner of the Eiswarnung package](https://raw.githubusercontent.com/klaasnicolaas/python-eiswarnung/main/assets/header_eiswarnung-min.png)

<!-- PROJECT SHIELDS -->
[![GitHub Release][releases-shield]][releases]
[![Python Versions][python-versions-shield]][pypi]
![Project Stage][project-stage-shield]
![Project Maintenance][maintenance-shield]
[![License][license-shield]](LICENSE)

[![GitHub Activity][commits-shield]][commits-url]
[![PyPi Downloads][downloads-shield]][downloads-url]
[![GitHub Last Commit][last-commit-shield]][commits-url]
[![Open in Dev Containers][devcontainer-shield]][devcontainer]

[![Code Quality][code-quality-shield]][code-quality]
[![Build Status][build-shield]][build-url]
[![Typing Status][typing-shield]][typing-url]

[![Maintainability][maintainability-shield]][maintainability-url]
[![Code Coverage][codecov-shield]][codecov-url]

Asynchronous Python client for the Eiswarnung API.

## About

A python package with which you can read data from [Eiswarnung API][eiswarnung]. This way you know whether it is necessary to scratch your car window the next day, because there is a layer of ice on it. This service comes from Germany but should work in other countries as well.

## Installation

```bash
pip install eiswarnung
```

## Usage

For a successful request, you must fill in the `latitude` and `longitude` data and have a valid `API key`, which you can request via [this website][request]. **Note**: there is a limit of 50 requests per day.

```py
import asyncio

from eiswarnung import Eiswarnung


async def main():
    """Show example on getting data from the Eiswarnung API."""
    async with Eiswarnung(
        api_key="API_KEY",
        latitude=49.17,
        longitude=11.10,
    ) as client:
        forecast = await client.forecast()
        print(forecast)
        print(client.ratelimit)


if __name__ == "__main__":
    asyncio.run(main())
```

## Data

You can read the following data with this package:

### Forecast

- Request date (datetime)
- Status ID (int)
- Forecast Type - in English (str)
- Forecast Text - in German (str)
- Forecast City (str)
- Forecast Date - the next day (datetime)

### Ratelimit

- Call Limit (int)
- Remaining Calls (int)
- Retry after (remaining seconds)

## Contributing

This is an active open-source project. We are always open to people who want to
use the code or contribute to it.

We've set up a separate document for our
[contribution guidelines](CONTRIBUTING.md).

Thank you for being involved! :heart_eyes:

## Setting up development environment

The simplest way to begin is by utilizing the [Dev Container][devcontainer]
feature of Visual Studio Code or by opening a CodeSpace directly on GitHub.
By clicking the button below you immediately start a Dev Container in Visual Studio Code.

[![Open in Dev Containers][devcontainer-shield]][devcontainer]

This Python project relies on [Poetry][poetry] as its dependency manager,
providing comprehensive management and control over project dependencies.

You need at least:

- Python 3.11+
- [Poetry][poetry-install]

### Installation

Install all packages, including all development requirements:

```bash
poetry install
```

_Poetry creates by default an virtual environment where it installs all
necessary pip packages_.

### Pre-commit

This repository uses the [pre-commit][pre-commit] framework, all changes
are linted and tested with each commit. To setup the pre-commit check, run:

```bash
poetry run pre-commit install
```

And to run all checks and tests manually, use the following command:

```bash
poetry run pre-commit run --all-files
```

### Testing

It uses [pytest](https://docs.pytest.org/en/stable/) as the test framework. To run the tests:

```bash
poetry run pytest
```

To update the [syrupy](https://github.com/tophat/syrupy) snapshot tests:

```bash
poetry run pytest --snapshot-update
```

## License

MIT License

Copyright (c) 2021-2025 Klaas Schoute

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

<!-- PROJECT -->
[eiswarnung]: https://www.eiswarnung.de
[request]: https://www.eiswarnung.de/get-api

<!-- MARKDOWN LINKS & IMAGES -->
[build-shield]: https://github.com/klaasnicolaas/python-eiswarnung/actions/workflows/tests.yaml/badge.svg
[build-url]: https://github.com/klaasnicolaas/python-eiswarnung/actions/workflows/tests.yaml
[code-quality-shield]: https://github.com/klaasnicolaas/python-eiswarnung/actions/workflows/codeql.yaml/badge.svg
[code-quality]: https://github.com/klaasnicolaas/python-eiswarnung/actions/workflows/codeql.yaml
[commits-shield]: https://img.shields.io/github/commit-activity/y/klaasnicolaas/python-eiswarnung.svg
[commits-url]: https://github.com/klaasnicolaas/python-eiswarnung/commits/main
[codecov-shield]: https://codecov.io/gh/klaasnicolaas/python-eiswarnung/branch/main/graph/badge.svg?token=w0pbSPjFIZ
[codecov-url]: https://codecov.io/gh/klaasnicolaas/python-eiswarnung
[devcontainer-shield]: https://img.shields.io/static/v1?label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode
[devcontainer]: https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/klaasnicolaas/python-eiswarnung
[downloads-shield]: https://img.shields.io/pypi/dm/eiswarnung
[downloads-url]: https://pypistats.org/packages/eiswarnung
[license-shield]: https://img.shields.io/github/license/klaasnicolaas/python-eiswarnung.svg
[last-commit-shield]: https://img.shields.io/github/last-commit/klaasnicolaas/python-eiswarnung.svg
[maintenance-shield]: https://img.shields.io/maintenance/yes/2025.svg
[maintainability-shield]: https://api.codeclimate.com/v1/badges/d1c7f7b99ac0225c2e18/maintainability
[maintainability-url]: https://codeclimate.com/github/klaasnicolaas/python-eiswarnung/maintainability
[project-stage-shield]: https://img.shields.io/badge/project%20stage-experimental-yellow.svg
[pypi]: https://pypi.org/project/eiswarnung/
[python-versions-shield]: https://img.shields.io/pypi/pyversions/eiswarnung
[typing-shield]: https://github.com/klaasnicolaas/python-eiswarnung/actions/workflows/typing.yaml/badge.svg
[typing-url]: https://github.com/klaasnicolaas/python-eiswarnung/actions/workflows/typing.yaml
[releases-shield]: https://img.shields.io/github/release/klaasnicolaas/python-eiswarnung.svg
[releases]: https://github.com/klaasnicolaas/python-eiswarnung/releases

<!-- Development -->
[poetry-install]: https://python-poetry.org/docs/#installation
[poetry]: https://python-poetry.org
[pre-commit]: https://pre-commit.com
