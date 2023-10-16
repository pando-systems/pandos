from dataclasses import dataclass
from functools import wraps
from typing import (
    Callable,
    Generic,
    Generator,
    TypeVar,
)


from pandos.settings import get_logger
from pandos.exceptions import pandos_exceptions
from pandos.maturity import MaturityLevel


MaturityLevel.ALPHA.set_module(
    file=__file__,
    logger=get_logger(name=__name__)
)


A = TypeVar("A")
B = TypeVar("B")


@dataclass(frozen=True, slots=True)
class EitherFunctionWrapper(Generic[A]):
    target: Callable[..., A]

    def either(self, *args, **kwargs) -> 'Either[A]':
        try:
            return Right[A].from_value(x=self.target(*args, **kwargs))
        except Exception as e:
            return Left(exception=e)

    def __call__(self, *args, **kwargs) -> A:
        return self.target(*args, **kwargs)


class Either(Generic[A]):

    @classmethod
    def decorator(cls, function: Callable):
        return wraps(function, updated=())(EitherFunctionWrapper(target=function))

    def __iter__(self):
        match self:
            case right if isinstance(right, Right):
                yield from [right.value]
            case left if isinstance(left, Left):
                yield from []

    @classmethod
    def comprehension(cls, generator: Generator):
        try:
            return Either.from_value(x=next(generator))
        except Exception as e:
            return Left(exception=e)

    @classmethod
    def from_value(cls, x: A, disable_exception_to_left: bool = False) -> 'Either[A]':
        if not disable_exception_to_left and isinstance(x, Exception):
            return Left(exception=x)
        return Right(value=x)

    def flat_map(self, function: Callable[[A], 'Either[B]']) -> 'Either[B]':
        raise NotImplementedError

    def map(self, function: Callable[[A], B]) -> 'Either[B]':
        raise NotImplementedError

    def resolve(self) -> A:
        match self:
            case right if isinstance(right, Right):
                return right.value
            case left if isinstance(left, Left):
                raise left.exception
            case _:
                return pandos_exceptions.MONADS_EITHER_INCONSISTENCY.throw(
                    message="Either Monad inconsistency detected when calling `resolve` method."
                )


@dataclass(frozen=True, slots=True)
class Right(Either[A]):
    value: A

    def flat_map(self, function: Callable[[A], Either[B]]) -> Either[B]:
        # Consider that your right will transform to a left if an exception is encountered
        try:
            return function(self.value)
        except Exception as e:
            return Left(exception=e)

    def map(self, function: Callable[[A], B]) -> Either[B]:
        return self.flat_map(function=lambda value: Right[B].from_value(x=function(value)))


@dataclass(frozen=True, slots=True)
class Left(Either[A]):
    exception: Exception

    def flat_map(self, function: Callable[[A], Either[B]]) -> Either[B]:
        return Left(exception=self.exception)  # Propagate exception

    def map(self, function: Callable[[A], B]) -> Either[B]:
        return Left(exception=self.exception)  # Propagate exception
