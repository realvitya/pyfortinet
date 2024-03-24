# Installation

## Installing package

Released versions can be installed from pypi.org by using the `pip`. It all depends on the environment, but it's
advisable to create a separate venv for the tool. Reason is that it's heavily depending on Pydantic 2, which is not
straight back compatible with Pydantic 1. If a system uses Pydantic 1, installing this tool can break things.

```shell
# create a venv in local directory 'fmgsync'
$ python -m venv fortinet
# activate venv in linux
$ . fortinet/bin/activate
# same on windows
> fortinet/Script/activate
# update environment
(fortinet)$ python -m pip install -U pip
# install tool with all features
(fortinet)$ python -m pip install pyfortinet[rich]
```

## Installing from source

The tool can be installed from GitHub

```shell
# latest main branch
$ pip install git+https://github.com/realvitya/pyfortinet.git
# specific version tag
$ pip install git+https://github.com/realvitya/pyfortinet.git@v1.0.0
```

If you want editor mode for development purposes, I recommend forking the project, cloning and installing it:

```shell
# clone repo to local folder
$ git clone https://github.com/{YOURACC}/pyfortinet
# install repo in editor mode (changes will be reflected immediately)
$ pip install -e ./pyfortinet[dev]
```
