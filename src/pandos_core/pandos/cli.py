import os
import datetime as dt
from time import perf_counter
from dataclasses import dataclass
from typing import (
    Optional,
)

from pandos.version import (Version, version)


@dataclass(frozen=True, slots=True)
class CLI:
    version: Version = version

    def hello(self, name: Optional[str] = None):
        name = name or "world"
        return f"Hello, {name}!"
