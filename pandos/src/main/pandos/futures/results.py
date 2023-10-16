from time import perf_counter
from dataclasses import dataclass
from typing import (
    Callable,
    Generic,
    Optional,
    TypeVar,
)
from pandos.futures.enums import FutureStatus
from pandos.monads.either import (
    Either,
    Right,
    Left,
)


A = TypeVar("A")


@dataclass(frozen=False, slots=True)
class FutureResult(Generic[A]):
    status: FutureStatus
    value: Optional[Either[A]] = None
    raise_exception: bool = False
    exec_duration: Optional[float] = None
    _ts_perf_counter: Optional[float] = None

    @property
    def age(self) -> Optional[float]:
        if self._ts_perf_counter is None:
            return None
        return perf_counter() - self._ts_perf_counter

    def define_with(self, function: Callable[..., A], *args, **kwargs):
        start = perf_counter()
        # The idea of the try-except statement is to wrap the result value on an Either Monad. Nonetheless, consider
        # that the function evaluation might return any of the following scenarios:
        # - Scenario 1 (ideal): Any python value or exception -- there should be managed with the Either Monad
        # - Scenario 2: An either monad instance... use that value directly and update the status accordingly.
        # - Scenario 3: Another future... Still thinking about how to handle this best.
        try:
            # Apply the function evaluation! Consider that this section should be running on a different thread
            # therefore it should be non-blocking.
            match function(*args, **kwargs):
                case right if isinstance(right, Right):
                    self.value = right
                    self.status = FutureStatus.SUCCESS
                case left if isinstance(left, Left):
                    self.value = left
                    self.status = FutureStatus.FAILURE
                case value:
                    self.value = Right.from_value(x=value)
                    self.status = FutureStatus.SUCCESS

        except Exception as e:
            self.value = Left(exception=e)
            self.status = FutureStatus.FAILURE
            if self.raise_exception:
                raise
        finally:
            self._ts_perf_counter = perf_counter()
            self.exec_duration = self._ts_perf_counter - start
