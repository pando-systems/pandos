import enum
from typing import Any

from pandos.settings import get_logger
from pandos.maturity import MaturityLevel


logger = get_logger(name=__name__)


MaturityLevel.ALPHA.set_module(
    file=__file__,
    logger=logger,
)


# Inspired on:
# - https://github.com/python/cpython/blob/4d1f033986675b883b9ff14588ae6ff78fdde313/Lib/enum.py#L1265
# - https://docs.python.org/3.11/library/enum.html#enum.StrEnum
class TextEnum(str, enum.Enum):

    def __new__(cls, value: str):
        member = str.__new__(cls, value)
        member._value_ = value
        return member

    @staticmethod
    def _generate_next_value_(name: str, start: int, count: int, last_values: list[Any]) -> Any:
        return name.lower()
