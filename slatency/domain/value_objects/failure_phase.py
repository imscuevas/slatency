from enum import Enum

class FailurePhase(Enum):
    """
    An enumeration of the possible stages at which a request can fail.
    """
    DNS = "DNS"
    TCP_CONNECTION = "TCP Connection"
    TLS_HANDSHAKE = "TLS Handshake"
    REQUEST = "Request"
    RESPONSE = "Response"
