# pando-systems-core

Pando Systems - Core Implementation

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

And install the `pandos-core` library:

```commandline
$ pip install -e src/pandos_core
```

### Installing extension

The pandos library is composed by a set of packages named "extensions". Each extension represents a "semantic grouping"
of system components and "extends" the `pandos.system` module.

The two main extensions are:
* `ext_pandos_backend`: Contains the `Pandos Server` implementation.
* `ext_pandos_frontend`: Contains the `Pandos Frontend Worker` implementation.

You can install an extension in your local machine directly via pip:

```commandline
$ pip install -e src/<extension_name>
```
