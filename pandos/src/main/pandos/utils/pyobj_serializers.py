import codecs
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
                return dill.loads(codecs.decode(string.encode(), "base64"), **kwargs)
            case self.PICKLE:
                import pickle
                return pickle.loads(codecs.decode(string.encode(), "base64"), **kwargs)
        raise ValueError("Unrecognized deserialization framework: " + self.name)

    def dumps(self, obj: Any, **kwargs) -> str:
        match self:
            case self.DILL:
                import dill
                return codecs.encode(dill.dumps(obj, **kwargs), "base64").decode()
            case self.PICKLE:
                import pickle
                return codecs.encode(pickle.dumps(obj, **kwargs), "base64").decode()
        raise ValueError("Unrecognized serialization framework: " + self.name)
