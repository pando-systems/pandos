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

## Installation via Pip

You can install `pandos` directly via pip:

```commandline
$ pip install pandos
```

## Development Setup

Install the development dependencies:

```commandline
$ pip install -r requirements-develop.txt
```

And install the `pandos` library:

```commandline
$ PANDOS_DISABLE_MYPYC=1 pip install -e pandos
```

Alternatively, you can also build pandos into a python wheel:
* Build wheel: `(cd pandos; python setup.py bdist_wheel)`
* Install: `python -m pip install pandos/dist/pandos*.whl`

When installing directly with `pip install` vs `python wheel`? 
* The `pip install -e pandos` approach works best when you are modifying the codebase heavily and you want to get the updates ASAP into the python package without having to re-install. Consider that the `PANDOS_DISABLE_MYPYC` must always be activated (i.e., `1`).
* The `python wheel` approach works best when you want to have an static version of the codebase and potentially compiled as c-extension for performance gains.

