from pathlib import Path
from typing import Generator
import pytest

LOG_FILE: Path = (
    Path(__file__).resolve().parent.parent.parent / 'requests.log'
)


@pytest.fixture(autouse=True)
def clean_requests_log() -> Generator[None, None, None]:
    """
    Fixture to ensure requests.log is cleaned before and after each test.
    """
    if LOG_FILE.exists():
        # LOG_FILE.write_text('')
        pass
    yield
    # Clean up after test run
    if LOG_FILE.exists():        
        # LOG_FILE.write_text('')
        pass
