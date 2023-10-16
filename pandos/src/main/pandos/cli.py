import os
import datetime as dt
import logging
from time import perf_counter
from dataclasses import dataclass
from types import TracebackType
from typing import (
    Any,
    Optional,
    Type,
    Union,
)

from pandos.version import Version, version
from pandos.settings import get_logger


logger = get_logger(name=__name__)


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

    @property
    def about(self) -> str:
        return f"Pandos Version: {self.version.value}"

    def environ(self, varname: str) -> Optional[str]:
        return os.environ.get(varname)

    def hello(self, name: Optional[str] = None):
        name = name or "world"
        return f"Hello, {name}!"

    def __enter__(self):
        logger.debug("Entering Pandos CLI context manager")
        logger.info(self.about)
        logger.info("Pandos start timestamp %s", self.now)
        return self

    def __exit__(
            self,
            exc_type: Optional[Type[Exception]] = None,
            exc_value: Optional[Exception] = None,
            exc_tb: Optional[TracebackType] = None,
    ):
        duration = self.duration
        status = "success" if exc_value is None else "failure"
        logger.info("Pandos command execution status: %s", status)
        logger.info("Pandos command execution duration: %f", duration)

    def execute(self, command: str, *args, **kwargs) -> Any:
        with self as cli:
            executable = getattr(cli, command)
            logger.info("Pandos command: %s", command)
            out = executable(*args, **kwargs)
        return out
