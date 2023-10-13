# Pandos

This is the `pandos` python package by Pando Systems.


* Developed with python version: `3.10.12`
* User guide [here](USER_GUIDE.md).

## (Recommended) Configure Python environment with pyenv

Define the python version to use in the repository. Consider reading
this [reference](https://rhdzmota.com/post/the-best-way-to-install-python/) if you don't have pyenv installed in your machine.

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

Alternatively, you can also build pandos into a python wheel:
* Build wheel: `(cd pandos; python setup.py bdist_wheel)`
* Install: `python -m pip install pandos/dist/pandos*.whl`

