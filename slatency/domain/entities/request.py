from dataclasses import dataclass
from typing import Dict, Optional

from slatency.domain.value_objects.url import URL
from slatency.domain.value_objects.http_method import HTTPMethod

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
