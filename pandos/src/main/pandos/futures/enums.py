import enum


class FutureStatus(enum.Enum):
    PENDING = -1
    FAILURE = 0
    SUCCESS = 1
