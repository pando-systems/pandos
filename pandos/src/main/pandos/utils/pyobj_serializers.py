from enum import auto
from typing import Any

from pandos.settings import get_logger
from pandos.maturity import MaturityLevel
from pandos.utils.custom_enum_types import TextEnum


logger = get_logger(name=__name__)


MaturityLevel.ALPHA.set_module(
    file=__file__,
    logger=logger,
)


class PyObjSerializationFrameworkEnum(TextEnum):
    DILL = auto()
    PICKLE = auto()

    def loads(self, string: str, **kwargs):
        match self:
            case self.DILL:
                import dill
                return dill.loads(string, **kwargs)
            case self.PICKLE:
                import pickle
                return pickle.loads(string, **kwargs)
        raise ValueError("Unrecognized deserialization framework: " + self.name)

    def dumps(self, obj: Any, **kwargs):
        match self:
            case self.DILL:
                import dill
                return dill.dumps(obj, **kwargs)
            case self.PICKLE:
                import pickle
                return pickle.loads(streing, **kwargs)
        raise ValueError("Unrecognized serialization framework: " + self.name)
