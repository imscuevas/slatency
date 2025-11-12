from dataclasses import dataclass, field
from typing import List
from uuid import UUID, uuid4

from slatency.domain.entities.request import Request
from slatency.domain.entities.response import Response


@dataclass
class Test:
    """
    A Test represents a scenario for sending a specific request multiple times
    and collecting its responses.
    """
    request: Request
    expected_responses: int
    responses: List[Response] = field(default_factory=list)
    test_id: UUID = field(default_factory=uuid4)
