import os
from setuptools import setup, find_namespace_packages
from typing import (
    List,
)


with open("README.md", "r") as file:
    readme = file.read()

with open("requirements.txt", "r") as file:
    requirements = [req for req in file.read().splitlines() if req and not req.startswith("#")]

with open(os.path.join("pandos", "version"), "r") as file:
    version = file.read().strip()

with open("LICENSE", "r") as file:
    license_content = file.read()


def get_packages(here: str = ".", pandos_prefix: str = "pandos") -> List[str]:
    return [
        package
        for package in find_namespace_packages(where=here)
        if package.startswith(pandos_prefix)
    ]


setup(
    name="pandos",
    version=version,
    description=(
        "The `pandos core` package contains the baseline implementation of the pandos base abstractions."
    ),
    long_description=readme,
    long_description_content_type="text/markdown",
    author="rhdzmota",
    author_email="info@rhdzmota.com",
    url="rhdzmota.com/pandos",
    # https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Typing :: Typed",
        "Topic :: Scientific/Engineering",
        "Topic :: System :: Distributed Computing",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.10",
    ],
    package_data={
        "": [
            "version",
        ]
    },
    include_package_data=True,
    packages=get_packages(),
    scripts=[
        "bin/pandos"
    ],
    install_requires=requirements,
    python_requires=">=3.10, <4",
    license=license_content,
)
