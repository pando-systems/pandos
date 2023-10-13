import uuid
from threading import Thread
from typing import (
    Callable,
    ClassVar,
    Dict,
    Generic,
    Optional,
    Tuple,
    TypeVar,
)

from pandos.futures.enums import FutureStatus
from pandos.futures.results import FutureResult


A = TypeVar("A")


class FutureStore(Generic[A]):
    _instance: ClassVar[Optional['FutureStore']] = None
    registry: ClassVar[Dict[str, FutureResult]] = {}
    # Undefined instance attributes
    expiration_once_realized_in_seconds: Optional[int]
    max_size: Optional[int]
    max_age: int

    # Singleton Pattern
    def __new__(
            cls,
            expiration_once_realized_in_seconds: Optional[int] = None,
            max_size: Optional[int] = None,
            max_age: int = 100_000,
    ):
        if cls._instance is None:
            cls._instance = super(FutureStore, cls).__new__(cls)
            # Instance attributes here:
            cls._instance.expiration_once_realized_in_seconds = expiration_once_realized_in_seconds
            cls._instance.max_size = max_size
            cls._instance.max_age = max_age
        return cls._instance

    @property
    def successes(self) -> int:
        return len([future for future in self.registry.values() if future.status == FutureStatus.SUCCESS])

    @property
    def failures(self) -> int:
        return len([future for future in self.registry.values() if future.status == FutureStatus.FAILURE])

    @property
    def unrealized(self) -> int:
        return len([future for future in self.registry.values() if future.status == FutureStatus.PENDING])

    def register(self, function: Callable[..., A], *args, **kwargs) -> Tuple[Thread, str]:
        if self.max_size is not None and len(self.registry) > self.max_size:
            # Think about this... do we really need to drop old futures?
            [
                self.registry.pop(key)
                for key, val in self.registry.items()
                if val.age and val.age > self.max_age
            ]
        # Register future
        future_id = str(uuid.uuid4())
        self.registry[future_id] = FutureResult(status=FutureStatus.PENDING)
        # Create thread
        thread = Thread(target=lambda: self.registry[future_id].define_with(function, *args, **kwargs), daemon=True)
        thread.start()
        return thread, future_id
