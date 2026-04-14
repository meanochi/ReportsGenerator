class AttendanceAppError(Exception):
    """Base exception for the attendance modifier application."""
    pass

class ClassificationError(AttendanceAppError):
    """Raised when the report type cannot be determined."""
    pass

class ParsingError(AttendanceAppError):
    """Raised when parsing the report text fails."""
    pass