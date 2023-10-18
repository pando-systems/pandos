import os
from setuptools import setup, find_namespace_packages
from typing import (
    List,
    Optional,
)


# Environ variables
PANDOS_CODEBASE_PATH = os.environ.get(
    "PANDOS_CODEBASE_PATH",
    default=os.path.join("src", "main")
)
PANDOS_DISABLE_MYPYC = int(os.environ.get(
    "PANDOS_DISABLE_MYPYC",
    default="0",
))
PANDOS_SETUP_MOCK = int(os.environ.get(
    "PANDOS_SETUP_MOCK",
    default="0",
))


if not PANDOS_DISABLE_MYPYC:
    from mypyc.build import mypycify


with open("README.md", "r") as file:
    readme = file.read()


with open("requirements.txt", "r") as file:
    requirements = [req for req in file.read().splitlines() if req and not req.startswith("#")]


with open(os.path.join(PANDOS_CODEBASE_PATH, "pandos", "version"), "r") as file:
    version = file.read().strip()


with open("LICENSE", "r") as file:
    license_content = file.read()


def get_source_files(
    ignore_mark: Optional[str] = None,
    skip_dirs: Optional[List[str]] = None,
    skip_files: Optional[List[str]] = None,
) -> List[str]:
    skip_dirs = skip_dirs or []
    skip_files = skip_files or []

    def traverse(path: str):
        for _, dirs, files in os.walk(path):
            node_files = [
                os.path.join(path, file)
                for file in files
                if file.endswith(".py") and file not in skip_files
            ]
            return node_files + [
                file
                for directory in dirs
                for file in traverse(os.path.join(path, directory))
                if directory not in skip_dirs
            ]
    return [
        source_file_handler.close() or source_file
        for source_file in traverse(PANDOS_CODEBASE_PATH)
        for source_file_handler in [open(source_file, "r")]
        if ignore_mark is None or ignore_mark not in source_file_handler.read()
    ]


def get_packages(here: str = ".", pandos_prefix: str = "pandos") -> List[str]:
    return [
        package
        for package in find_namespace_packages(where=here)
        if package.startswith(pandos_prefix)
    ]


mypyc_configs = [
    # "--disallow-untyped-defs",  # TODO: Enable this option eventually for better performance
    "--ignore-missing-imports",
]


mypyc_target_files = get_source_files(
    ignore_mark="# pandos-mypyc-ignore-file",
    skip_dirs=[
        "__pycache__",
    ],
    skip_files=[
        "__init__.py"
    ],
)


packages = get_packages(here=PANDOS_CODEBASE_PATH)


if not PANDOS_SETUP_MOCK:
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
        url="https://github.com/pando-systems/pandos",
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
        package_dir={
            "": PANDOS_CODEBASE_PATH,
        },
        package_data={
            "": [
                "version",
            ]
        },
        include_package_data=True,
        packages=packages,
        scripts=[
            os.path.join("bin", "pandos"),
        ],
        install_requires=requirements,
        python_requires=">=3.10, <4",
        license=license_content,
        zip_safe=False,
        **({} if PANDOS_DISABLE_MYPYC else dict(ext_modules=mypycify(mypyc_configs + mypyc_target_files))),
    )
else:
    # This is temporal, we should eventually remove this!
    import json

    debugging_info = {
        "packages": packages,
        "mypyc_configs": mypyc_configs,
        "mypyc_target_files": mypyc_target_files,
    }

    print(json.dumps(debugging_info, default=str, indent=4))
