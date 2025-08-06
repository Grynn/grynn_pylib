# grynn_pylib

[![PyPI version](https://img.shields.io/pypi/v/grynn_pylib.svg)](https://pypi.org/project/grynn_pylib/)
[![Python Tests](https://github.com/Grynn/grynn_pylib/actions/workflows/pytest.yml/badge.svg?branch=main)](https://github.com/Grynn/grynn_pylib/actions/workflows/pytest.yml)

This is a Python library project that provides finance-related functions and general utility functions.

## Installation

You can install the library using uv (or pip):

```shell
uv install grynn_pylib
#OR
pip install grynn_pylib
```

## Usage

```python
from grynn_pylib import utils

pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
utils.bcompare(pd.a, pd.b)
```

## Development & Publishing

### Publishing to PyPI

This package is automatically published to PyPI when a new version tag is pushed to the repository:

1. Update the version in `pyproject.toml`
2. Create and push a version tag:
   ```bash
   git tag v0.3.4  # Use the new version number
   git push origin v0.3.4
   ```
3. The GitHub Actions workflow will automatically build and publish the package to PyPI

**Note**: The repository must have a `PYPI_API_TOKEN` secret configured in GitHub Settings > Secrets and variables > Actions for automated publishing to work.

## License

This project is licensed under the MIT License. See the [LICENSE](https://github.com/grynn/grynn_pylib/blob/main/LICENSE) file for more information.

## Notes

* This project is a work in progress.
* py_vollib could be an alternative to the Black-Scholes formula implementation in this library.
* [optlib](https://github.com/dbrojas/optlib/tree/master) looks interesting (uses a very old numpy though, did not install on 3.12.6 out of the box)
