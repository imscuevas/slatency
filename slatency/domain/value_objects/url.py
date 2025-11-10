from dataclasses import dataclass
from typing import Dict

@dataclass(frozen=True)
class URL:
    """
    A URL represents a Uniform Resource Locator.
    """
    protocol: str
    host: str
    port: int
    path: str
    query_params: Dict[str, str]
