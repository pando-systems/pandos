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
    _start_performance_counter: float = perf_counter()
    _now: dt.datetime = dt.datetime.utcnow()

    @property
    def duration(self) -> float:
        return perf_counter() - self._start_performance_counter

    @property
    def now(self) -> str:
        return self._now.isoformat()

    def environ(self, varname: str) -> Optional[str]:
        return os.environ.get(varname)

    def hello(self, name: Optional[str] = None):
        name = name or "world"
        return f"Hello, {name}!"
