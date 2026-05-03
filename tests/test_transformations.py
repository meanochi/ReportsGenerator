"""Unit tests for transformation logic."""
import pytest
from dataclasses import FrozenInstanceError
from src.domain.models import AttendanceRow

def test_attendance_row_immutable():
    """Test that AttendanceRow is frozen (immutable)."""
    row = AttendanceRow(
        date="01/01/2024",
        original_in="09:00",
        original_out="17:00",
        raw_text_line="01/01/2024 09:00 17:00"
    )
    with pytest.raises(FrozenInstanceError):
        row.date = "02/01/2024"

def test_attendance_row_creation():
    """Test creating an AttendanceRow."""
    row = AttendanceRow(
        date="01/01/2024",
        original_in="09:00",
        original_out="17:00",
        raw_text_line="01/01/2024 09:00 17:00"
    )
    assert row.date == "01/01/2024"
    assert row.original_in == "09:00"
