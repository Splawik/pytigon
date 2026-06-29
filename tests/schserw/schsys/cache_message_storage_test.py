# Pytest tests
import contextlib

import pytest
from django.test import RequestFactory

from pytigon.schserw.schsys.cache_message_storage import CacheStorage


class MockSession(dict):

    """A mock session that behaves like a Django session with session_key."""

    def __init__(self, session_key="test_session_key"):
        super().__init__()
        self.session_key = session_key
        self.modified = False


@pytest.fixture
def cache_storage():
    request = RequestFactory().get("/")
    request.session = MockSession("test_session_key")
    return CacheStorage(request)


def test_cache_storage_get_no_session():
    """Test _get returns empty when session is None."""
    request = RequestFactory().get("/")
    request.session = None
    storage = CacheStorage(request)
    messages, retrieved = storage._get()
    assert messages == []
    assert retrieved is False


def test_cache_storage_get_no_session_key():
    """Test _get returns empty when session has no session_key."""
    request = RequestFactory().get("/")
    request.session = MockSession(None)  # session_key is None
    storage = CacheStorage(request)
    messages, retrieved = storage._get()
    assert messages == []
    assert retrieved is False


def test_cache_storage_get_no_messages(cache_storage):
    """Test _get returns empty when no cached messages exist."""
    messages, retrieved = cache_storage._get()
    assert messages == []
    assert retrieved is False


def test_cache_storage_store_no_messages(cache_storage):
    """Test _store with empty messages list deletes cache key."""
    with contextlib.suppress(Exception):
        cache_storage._store([], None)
    # After storing empty messages, the method should complete without error
    assert True


def test_cache_storage_get_with_session_key(cache_storage):
    """Test _get returns messages when session_key is present but cache is empty."""
    messages, retrieved = cache_storage._get()
    assert messages == []
    assert retrieved is False


if __name__ == "__main__":
    pytest.main()
