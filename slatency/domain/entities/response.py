from dataclasses import dataclass, field
from typing import Union
from uuid import UUID, uuid4

from slatency.domain.value_objects.failure_phase import FailurePhase
from slatency.domain.value_objects.flow import Flow
from slatency.domain.value_objects.latency import Latency


@dataclass
class SuccessfulResponse:
    """
    Represents a successful HTTP response.
    """
    status_code: int
    latency: Latency
    flow: Flow
    response_id: UUID = field(default_factory=uuid4)


@dataclass
class FailedResponse:
    """
    Represents a failed HTTP request.
    """
    failure_phase: FailurePhase
    error_message: str
    response_id: UUID = field(default_factory=uuid4)


Response = Union[SuccessfulResponse, FailedResponse]
