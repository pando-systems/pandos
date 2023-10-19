import enum
from typing import ClassVar, Optional, Type

from pandos.settings import get_logger
from pandos.maturity import MaturityLevel


logger = get_logger(name=__name__)


MaturityLevel.ALPHA.set_module(
    file=__file__,
    logger=logger
)


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
    default_message: ClassVar[str] = "Pandos Generic Exception"

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
            FUTURES_UNRESOLVED_ERROR=cls.custom(
                exception_name="PandosFuturesUnresolvedError",
                default_message="The future has not been resolved yet."
            ),
            FUTURES_INCONSISTENT_ERROR=cls.custom(
                exception_name="PandosFuturesInconsistentError",
                default_message="An inconsistent future was detected... this should not happen."
            ),
            FUTURES_INVALID_STATE_ERROR=cls.custom(
                exception_name="PandosFuturesInvalidStateError",
                default_message="Future match-statement detected an invalid state... this should never happen.",
            ),
            FEATURE_MATURITY_LEVEL_UNDEFINED=cls.custom(
                exception_name="PandosFeatureMaturityLevelUndefined",
                default_message="Feature maturity level undefined... this should not happen!"
            ),
            FEATURE_MATURITY_LEVEL_UNDEFINED_MESSAGE_INCONSISTENCY=cls.custom(
                exception_name="PandosFeatureMaturityLevelUndefinedMessageInconsistency",
                default_message="The feature maturity level being used should have a message template."
            ),
        )


pandos_exceptions = PandosException.enums()
