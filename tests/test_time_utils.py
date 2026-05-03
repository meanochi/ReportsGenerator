"""Unit tests for time utility functions."""
import pytest
from datetime import datetime
from utils.time_utils import str_to_time, time_to_str, get_deterministic_delta

def test_str_to_time():
    """Test converting time string to datetime."""
    result = str_to_time("14:30")
    assert result.hour == 14
    assert result.minute == 30

def test_time_to_str():
    """Test converting datetime to time string."""
    dt = datetime.strptime("14:30", "%H:%M")
    result = time_to_str(dt)
    assert result == "14:30"

def test_deterministic_delta_same_input():
    """Test that same input produces same delta."""
    delta1 = get_deterministic_delta("01/01/2024", "in")
    delta2 = get_deterministic_delta("01/01/2024", "in")
    assert delta1 == delta2

def test_deterministic_delta_different_salt():
    """Test that different salt produces different delta."""
    delta_in = get_deterministic_delta("01/01/2024", "in")
    delta_out = get_deterministic_delta("01/01/2024", "out")
    assert delta_in != delta_out

def test_deterministic_delta_in_range():
    """Test that delta is within expected range."""
    delta = get_deterministic_delta("01/01/2024", "in")
    assert -15 <= delta <= 15
