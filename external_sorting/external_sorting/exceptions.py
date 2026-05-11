"""Custom exceptions for the external sorting library."""


class ExternalSortingError(Exception):
    """Base exception for all library errors."""
    pass


class InvalidFileFormatError(ExternalSortingError):
    """Raised when a file format is not supported."""
    pass


class MemoryLimitError(ExternalSortingError):
    """Raised when an operation would exceed memory limits."""
    pass