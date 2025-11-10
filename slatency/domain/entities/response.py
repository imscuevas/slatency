from dataclasses import dataclass
from typing import Union

from slatency.domain.value_objects.flow import Flow
from slatency.domain.value_objects.latency import Latency
from slatency.domain.value_objects.failure_phase import FailurePhase

@dataclass
class SuccessfulResponse:
    """
    Represents a successful HTTP response.
    """
    status_code: int
    latency: Latency
    flow: Flow

@dataclass
class FailedResponse:
    """
    Represents a failed HTTP request.
    """
    failure_phase: FailurePhase
    error_message: str

Response = Union[SuccessfulResponse, FailedResponse]
