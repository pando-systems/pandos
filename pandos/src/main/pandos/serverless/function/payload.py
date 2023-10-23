import time
import json
import uuid
from dataclasses import dataclass
from typing import (
    List,
    Dict,
    Tuple,
    Optional,
)

import requests

from pandos.system.toolbox.endpoints import BackendEndpoints
from ...futures.future import Future


def payload_evaluation_callback(function_name: str, payload_uuid: str, wait: int) -> Dict:
    time.sleep(wait)
    url = BackendEndpoints.SERVERLESS_FUNCTION_EVALUATION.url(
        user_name="default",
        function_name=function_name,
        payload_uuid=payload_uuid,
    )
    response = requests.get(url)
    response_payload = response.json()
    if response.ok:
        return response_payload
    elif response_payload["status"] == "PENDING":
        return payload_evaluation_callback(
            function_name=function_name,
            payload_uuid=payload_uuid,
            wait=wait,
        )
    else:
        raise ValueError(f"Payload Retrieve Issue ({response.status_code}): {response.text}")


@dataclass(frozen=True, slots=True)
class Payload:
    function_name: str
    args: Optional[List] = None
    kwargs: Optional[Dict] = None

    def get_payload(self) -> Dict:
        return {
            "args": list(self.args) if self.args else [],
            "kwargs": self.kwargs or {}
        }

    def serialize(self, **kwargs) -> Tuple[str, str]:
        return (payload_serialized := json.dumps(self.get_payload(), **kwargs)), str(uuid.uuid5(
            uuid.NAMESPACE_OID,
            payload_serialized
        ))

    def evaluate(self) -> Future[Dict]:
        payload_uuid, payload_serialized = self.serialize()
        url = BackendEndpoints.SERVERLESS_FUNCTION_EVALUATION.url(
            user_name="default",
            function_name=function_name,
            payload_uuid=payload_uuid,
        )
        response = requests.post(
            url=url,
            json=payload_serialized,
        )
        if not response.ok:
            raise ValueError(f"Payload Submit Issue ({response.status_code}): {response.text}")
        response_payload = response.json()
        return Future(
            function=lambda: payload_evaluation_callback(
                function_name=self.function_name,
                payload_uuid=payload_uuid,
                wait=response_payload.get("wait") or 1
            )
        )
