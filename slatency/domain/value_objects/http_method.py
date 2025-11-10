from enum import Enum

class HTTPMethod(Enum):
    """
    An enumeration of supported HTTP methods.
    """
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    PATCH = "PATCH"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
