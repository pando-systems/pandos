import os
import datetime as dt
from time import perf_counter
from dataclasses import dataclass
from types import TracebackType
from typing import (
    Any,
    Optional,
    Type,
)

from pandos.version import Version, version
from pandos.maturity import MaturityLevel
from pandos.settings import get_logger


logger = get_logger(name=__name__)


MaturityLevel.ALPHA.set_module(
    file=__file__,
    logger=logger
)


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

    def feature_maturity(self, module: str):
        # TODO: Improve implementation...
        #       ATM we are just triggering the log function by importing the module by name
        import importlib

        importlib.import_module(module)

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

    @classmethod
    def system(cls, syscli: str) -> Type:
        import importlib

        module_name = ".".join(["pandos", "system", syscli, "syscli"])
        module_reference = importlib.import_module(module_name)
        cls_ext = getattr(module_reference, "CLIExtension")
        return type("CLI" + syscli.title(), (cls_ext, cls), {
            "pandos_version": cls().version.value,
        })
