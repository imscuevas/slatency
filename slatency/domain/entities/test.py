from dataclasses import dataclass, field
from typing import List

from slatency.domain.entities.request import Request
from slatency.domain.entities.response import Response


@dataclass
class Test:
    """
    A Test represents a scenario for sending a specific request multiple times
    and collecting its responses.
    """
    request: Request
    responses: List[Response] = field(default_factory=list)
