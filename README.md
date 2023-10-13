# Pandos

This is the `pandos` python package by Pando Systems.


* Developed with python version: `3.10.12`


## Configure Python environment with pyenv

Define the python version to use in the repository.

```commandline
$ pyenv local 3.10.12
```
* You may have to install before with: `pyenv install 3.10.12`

Create a virtualenv:

```commandline
$ pyenv exec python -m venv venv
```
* Activate command for MacOS/Linux: `source venv/bin/activte`
* Activate command for Win: `source venv/Scripts/activate`
* Deactivate: `deactivate`


## Development Setup

Install the development dependencies:

```commandline
$ pip install -r requirements-develop.txt
```

And install the `pandos` library:

```commandline
$ pip install -e pandos
```

## User Guide

[User guide referece here](USER_GUIDE.md)

