# test.py

from datetime import timedelta

def set_datetime():
    """Set current datetime."""
    from main import TEST_MODE, test_time
    return test_time if TEST_MODE else __import__('datetime').datetime.now()

def advance_time(seconds):
    """Advance test time."""
    from main import TEST_MODE
    if TEST_MODE:
        import main
        main.test_time += timedelta(seconds=seconds)