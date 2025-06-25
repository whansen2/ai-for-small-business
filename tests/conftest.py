import pytest
import time

@pytest.fixture(autouse=True)
def sleep_between_tests():
    yield
    time.sleep(1)  # Sleep for 1 second between tests to avoid rate limits
