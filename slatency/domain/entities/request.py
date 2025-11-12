from dataclasses import dataclass, field
from typing import Dict, Optional
from uuid import UUID, uuid4

from slatency.domain.value_objects.http_method import HTTPMethod
from slatency.domain.value_objects.url import URL


@dataclass
class Request:
    """
    A Request represents an HTTP request to be sent to a target service.
    """
    url: URL
    method: HTTPMethod
    headers: Dict[str, str]
    body: Optional[bytes]
    timeout: int = 10
    request_id: UUID = field(default_factory=uuid4)
