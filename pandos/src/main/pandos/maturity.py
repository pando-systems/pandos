import os
import enum
from logging import Logger
from dataclasses import dataclass
from typing import Optional

from pandos.settings import get_logger
from pandos.settings import (
    PANDOS_DISABLE_FEATURE_MATURITY_LOGS,
)


logger = get_logger(name=__name__)


# pandos-mypyc-ignore-file
# TODO: This file is ingored due to the following mypyc error:
#       Non-extension classes may not inherit from extension classes.
#       There's an on-going thread in github to fix this: https://github.com/python/mypy/issues/9612
@dataclass(frozen=True)
class FeatureMaturity:
    tag: str
    message: Optional[str]
    description: str
    loglevel: str

    @property
    def maturity_level(self) -> 'MaturityLevel':
        return MaturityLevel[self.tag]

    def set_module(
            self,
            file: str,
            logger: Logger
    ):
        # Early exit if the maturity level logs are disabled
        if PANDOS_DISABLE_FEATURE_MATURITY_LOGS:
            return
        # Get the module name from the reference file path
        root, part, module = file.partition(os.path.join("src", "main", "pandos", ""))
        if module.endswith("__init__.py"):
            module = os.path.dirname(module)
        # Verify if we have a message template
        if not self.message:
            if self.maturity_level.code < 1:
                from pandos.exceptions import pandos_exceptions  # Lazy import

                pandos_exceptions.FEATURE_MATURITY_LEVEL_UNDEFINED_MESSAGE_INCONSISTENCY.throw()
            return
        # Format the message template and pass it through the logs
        message = self.message.format(module=module)
        logger_function = getattr(logger, self.loglevel)
        logger_function(message)


class MaturityLevel(FeatureMaturity, enum.Enum):
    PRE_ALPHA = (
        "PRE_ALPHA",
        "You are using a pre-alpha feature: {module}",
        "Pre-Alpha status means that the feature still being figured out and in WIP status. "
        "This most likely results in incomplete/inconsistent features and non-stable interfaces. "
        "All changes regarding these features, even non-backward compatible changes, will be registered as patch.",
        "warning"
    )
    ALPHA = (
        "ALPHA",
        "You are using an alpha feature: {module}",
        "Alpha status means that the current feature is complete but still considered as experimental. "
        "Breaking changes can occur at any moment and documentation/testing is limited. "
        "All changes regarding these features, even non-backward compatible changes, will be registered as patch.",
        "warning"
    )
    BETA = (
        "BETA",
        "You are using a beta feature: {module}",
        "Beta status means that the feature is considered mature-enough to be used by technical & savvy users. "
        "At this point, the feature should be almost 100% complete but may still receive significant updates. "
        "We encourage users to submit feedback and bug reports since this will be the first time the feature will be "
        "used by a larger number of users. Technical documentation and unit-testing should be almost done by now. "
        "Consider that changes regarding these features, including non-backward compatible changes, "
        "will only affect the minor or patch values (`minor.patch`). If you see this message, you are still early "
        "to the development process! You can make a difference by letting us know your experience here: TBD",
        "warning"
    )
    GAMMA = (
        "GAMMA",
        None,
        "Gamma status means that the feature is considered mature-enough to be used by most users. "
        "The technical implementation of the feature is mostly over alongside with technical documentation "
        "and unit-testing. The feature is now being formally documented (end-user docs) and use-cases / examples are "
        "being made available. Extensive testing by our QA team is being done and semantic versioning is "
        "fully applied at this point (`major.minor.patch`).",
        "info"
    )
    STABLE = (
        "STABLE",
        None,
        "Stable status means that the feature is well-documented, has unit-testing, had passed QA and the "
        "interface/functionality are resilient to change. Changes are incorporated into the package-level versioning "
        "via semantic-versioning (`major.minor.patch`).",
        "debug"
    )
    TO_BE_DEPRECATED = (
        "TO_BE_DEPRECATED",
        "Danger zone! You are using a feature soon to be deprecated: {module}",
        "The 'To be Deprecated' status means that the feature (module) you are using will most likely be removed "
        "on the next major release.",
        "warning"
    )

    @property
    def code(self) -> int:
        match self:
            case self.PRE_ALPHA | self.ALPHA | self.BETA | self.TO_BE_DEPRECATED:
                return 0
            case self.GAMMA | self.STABLE:
                return 1
        from pandos.exceptions import pandos_exceptions  # Lazy import

        return pandos_exceptions.FEATURE_MATURITY_LEVEL_UNDEFINED.throw()


MaturityLevel.ALPHA.set_module(
    file=__file__,
    logger=logger
)
