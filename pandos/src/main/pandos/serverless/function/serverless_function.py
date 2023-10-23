from functools import wraps
from dataclasses import dataclass
from typing import (
    Callable,
    Tuple,
    Optional,
)

import requests

from ...utils.pyobj_serializers import PyObjSerializationFrameworkEnum
from pandos.system.toolbox.endpoints import BackendEndpoints


@dataclass(frozen=True, slots=True)
class ServerlessFunction:
    function: Callable
    overwrite_function_name: Optional[str] = None
    overwrite_serializer: Optional[PyObjSerializationFrameworkEnum] = None

    def __call__(self, *args, **kwargs):
        return self.function(*args, **kwargs)

    @property
    def name(self) -> str:
        return self.overwrite_function_name or self.function.__name__

    @property
    def serializer(self) -> PyObjSerializationFrameworkEnum:
        return self.overwrite_serializer or PyObjSerializationFrameworkEnum.DILL

    @property
    def url_registration(self) -> str:
        return BackendEndpoints.SERVERLESS_FUNCTIONS_REGISTER.url(user_name="default", function_name=self.name)

    @property
    def function_data(self) -> str:
        return self.serializer.dumps(self.function)

    @property
    def payload_registration(self):
        return {
            "function_data": self.function_data,
            "function_serialization_framework": self.serializer.name,
        }

    @classmethod
    def decorate(
            cls,
            overwrite_function_name: Optional[str] = None,
    ):
        def decorator(function: Callable):
            serverless_function = cls(
                function=function,
                overwrite_function_name=overwrite_function_name
            )
            ok, _ = serverless_function.register()
            if not ok:
                raise ValueError("ERROR!!!")
            return serverless_function  #TODO: wraps(function, updated=())(serverless_function)
        return decorator

    def register(
            self,
    ) -> Tuple[bool, requests.Response]:
        response = requests.post(
            self.url_registration,
            json=self.payload_registration,
        )
        return response.ok, response

    def submit(self, *args, **kwargs):
        from .payload import Payload

        payload = Payload(function_name=self.name, args=list(args) if args else None, kwargs=kwargs)
        return payload.evaluate()
