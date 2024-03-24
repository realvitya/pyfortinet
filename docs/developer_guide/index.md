# Developer Guide

First, thank you for being interested in developing this library! The following topics tries to describe the intended
setup and workflow to develop the library!

## Installing dev tools

For development, you can use the project framework by installing the library with `dev` extras:

```shell
# clone your fork
git clone https://github.com/{YOURFORK}/pyfortinet.git
# install in edit mode
pip install -e ./pyfortinet[dev]
```

## Using Invoke

The project uses [Invoke](https://www.pyinvoke.org/) for common tasks. You may check all tasks supported in the
`tasks.py` config file.

### Run linters

Linters are invoked by pre-commit which is installed with the dev tools.

### Start mkdocs server
