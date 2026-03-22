from src.utils import sanitize
def test_sanitize():
    assert sanitize("Hello World!!!") == "Hello_World"
