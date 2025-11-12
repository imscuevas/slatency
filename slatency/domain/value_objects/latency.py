from dataclasses import dataclass


@dataclass(frozen=True)
class Latency:
    """
    A value object holding detailed timing information for a successful request.
    All values are in milliseconds.
    """
    queue: int
    dns: int
    connect: int
    tls: int
    send_first_byte: int
    send_last_byte: int
    receive_first_byte: int
    total: int
