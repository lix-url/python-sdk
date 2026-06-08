class LixException(Exception):
    """Base exception for all Lix SDK errors."""
    pass


class HttpClientException(LixException):
    """Raised when an underlying HTTP transport error occurs."""
    pass


class NotFoundException(LixException):
    """Raised on HTTP 404 Not Found."""
    pass


class RateLimitException(LixException):
    """Raised on HTTP 429 Too Many Requests."""
    pass


class ServerException(LixException):
    """Raised on HTTP 500 Internal Server Error."""
    pass


class UnauthorizedException(LixException):
    """Raised on HTTP 401 Unauthorized."""
    pass


class ValidationException(LixException):
    """Raised on HTTP 400 Bad Request. Contains field-level error details."""

    def __init__(self, data):
        super().__init__('Validation error')
        self.data = data
