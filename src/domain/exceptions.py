class AttendanceAppError(Exception):
    """Base exception for the attendance modifier application."""


class ClassificationError(AttendanceAppError):
    """Raised when the report type cannot be determined."""


class ParsingError(AttendanceAppError):
    """Raised when parsing the report text fails."""


class TransformationError(AttendanceAppError):
    """Raised when a transformed row fails validation."""
