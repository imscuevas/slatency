from dataclasses import dataclass


@dataclass(frozen=True)
class Flow:
    """
    A value object containing the network flow information for a request.
    """
    source_ip: str
    source_port: int
    destination_ip: str
    destination_port: int