from functools import wraps
from dataclasses import dataclass
from typing import (
    Callable,
    Generic,
    Optional,
    TypeVar,
    Union,
)

from pandos.exceptions import pandos_exceptions
from pandos.futures.store import FutureStore
from pandos.futures.enums import FutureStatus
from pandos.monads.either import (
    Either,
    Right,
    Left,
)


A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True, slots=True)
class FutureFunctionWrapper:
    target: Callable[..., A]

    def future(self, *args, **kwargs) -> 'Future[A]':
        return Future[A](self.target, *args, **kwargs)

    def __call__(self, *args, **kwargs) -> A:  # type: ignore
        return self.target(*args, **kwargs)


class Future(Generic[A]):
    __slots__ = "thread", "future_id"

    def __init__(self, function: Callable[..., A], *args, **kwargs):
        self.thread, self.future_id = FutureStore().register(function, *args, **kwargs)

    def __str__(self) -> str:
        return self.future_id

    def __repr__(self) -> str:
        match FutureStore.registry[self.future_id].status:
            case FutureStatus.SUCCESS:
                return "Future[Success]"
            case FutureStatus.FAILURE:
                return "Future[Failure]"
            case FutureStatus.PENDING:
                return "Future[Pending]"
        # For some reason, the type check is expecting a return... raising an error instead
        return pandos_exceptions.FUTURES_INVALID_STATE_ERROR.throw()

    def __iter__(self):
        yield from [self.wait_and_resolve()]

    @classmethod
    def comprehension(cls, generator, timeout: Optional[int] = None):
        return Future(function=lambda: next(generator), timeout=timeout)

    @classmethod
    def decorator(cls, timeout: Optional[int] = None) -> Callable[[Callable[..., A]], FutureFunctionWrapper]:
        return lambda function: wraps(function, updated=())(FutureFunctionWrapper)(target=function)  # type: ignore

    @property
    def status(self) -> FutureStatus:
        return FutureStore.registry[self.future_id].status

    def _coerce_current_value(self) -> Either[A]:
        result = FutureStore.registry[self.future_id]
        match result.status:
            case FutureStatus.SUCCESS:
                return result.value
            case FutureStatus.FAILURE:
                print("Failure")
                return result.value
            case FutureStatus.PENDING:
                return pandos_exceptions.FUTURES_UNRESOLVED_ERROR.throw(
                    f"Trying to coerce value from unresolved future: {self.future_id}"
                )

    def wait(self, timeout: Optional[float] = None) -> Either[A]:
        self.thread.join(timeout=timeout)
        try:
            return self._coerce_current_value()
        except pandos_exceptions.FUTURES_UNRESOLVED_ERROR.value:
            return pandos_exceptions.FUTURES_INCONSISTENT_ERROR.throw(
                f"Future with inconsistent state detected in wait-call (should be resolved): {self.future_id}"
            )

    def wait_and_resolve(self, timeout: Optional[float] = None) -> A:
        return self.wait(timeout=timeout).resolve()

    def get(
            self,
            or_else: Optional[B] = None,
            blocking: bool = False,
            timeout:  Optional[float] = None
    ) -> Union[Either[A], Optional[B]]:
        # TODO: Should or_else apply only on unresolved (pending) futures or also on failed futures?
        if blocking:
            return self.wait(timeout=timeout)
        try:
            return self._coerce_current_value()
        except pandos_exceptions.FUTURES_UNRESOLVED_ERROR.value:
            # TODO: Logger?
            return or_else

    @classmethod
    def from_value(cls, x: A) -> 'Future[A]':
        return Future[A](lambda: x)

    def flat_map(self, function: Callable[[A], 'Future[B]'], timeout: Optional[float] = None) -> 'Future[B]':
        # This works, but is blocking: return function(self.wait_and_resolve())
        # The following implementation is just a placeholder and should be improved for performance.
        return Future(
            function=lambda: function(self.wait_and_resolve(timeout=timeout)).wait_and_resolve(timeout=timeout)
        )

    def map(self, function: Callable[[A], B], timeout: Optional[float] = None) -> 'Future[B]':
        return Future(
            function=lambda: function(self.wait_and_resolve(timeout=timeout))
        )
