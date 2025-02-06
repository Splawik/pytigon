from pytigon.schserw.schsys.cache_message_storage import *

# Pytest tests
import pytest
from django.contrib.messages.storage.base import Message
from django.test import RequestFactory


@pytest.fixture
def cache_storage():
    request = RequestFactory().get("/")
    request.session = {}
    return CacheStorage(request)


def test_cache_storage_get_no_session(cache_storage):
    cache_storage.request.session = None
    messages, retrieved = cache_storage._get()
    assert messages == []
    assert retrieved is False


def test_cache_storage_get_no_messages(cache_storage):
    messages, retrieved = cache_storage._get()
    assert messages == []
    assert retrieved is False


def test_cache_storage_store_no_messages(cache_storage):
    cache_storage._store([], None)
    cached_messages = cache.get("django_messages_test_session_key")
    assert cached_messages is None
