import enum
from typing import Optional, Type


class ExceptionEnumBuilder(enum.Enum):

    def throw(self, message: Optional[str] = None):
        raise self.value(message)

    @classmethod
    def members(cls, name: str, **kwargs):
        return cls(
            value=name,
            # type: ignore
            names=[
                (exc_name, exc_cls)
                for exc_name, exc_cls in kwargs.items()
            ]
        )


class PandosException(Exception):
    default_message: str = "Pandos Generic Exception"

    def __init__(self, message: Optional[str] = None):
        super().__init__(message or self.default_message)

    @classmethod
    def custom(
            cls,
            exception_name: str,
            default_message: Optional[str] = None,
    ) -> Type:
        attrs = {
            "default_message": default_message or cls.default_message
        }
        return type(exception_name, (cls,), attrs)

    @classmethod
    def enums(cls):
        return ExceptionEnumBuilder.members(
            name="PandosExceptionCatalog",
            # Register exceptions here:
            PANDOS_BUILTIN_CUSTOM_EXCEPTION=cls.custom(
                exception_name="PandosBuiltInCustomException",
                default_message="This is an example custom exception - you should not find this error message in prod",
            ),
            MONADS_EITHER_INCONSISTENCY=cls.custom(
                exception_name="PandosMonadsEitherInconsistency",
                default_message="Inconsistency detected in Either Monad",
            ),
        )


pandos_exceptions = PandosException.enums()
