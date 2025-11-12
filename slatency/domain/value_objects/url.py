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

    def __post_init__(self):
        if self.protocol not in ("http", "https"):
            raise ValueError("Protocol must be 'http' or 'https'")
        if not (0 <= self.port <= 65535):
            raise ValueError("Port must be between 0 and 65535")
