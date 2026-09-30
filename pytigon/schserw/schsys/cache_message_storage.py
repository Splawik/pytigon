import logging

from django.conf import settings
from django.contrib.messages.storage.session import SessionStorage
from django.core.cache import cache

logger = logging.getLogger(__name__)

#: Fallback lifetime (seconds) when ``MESSAGE_STORAGE_TTL`` is not configured.
DEFAULT_TTL = 60 * 60 * 24


def _get_ttl():
    """Return the cache TTL to use for stored messages, in seconds.

    Returns:
        int: The configured ``MESSAGE_STORAGE_TTL``, or :data:`DEFAULT_TTL`.
    """
    ttl = getattr(settings, "MESSAGE_STORAGE_TTL", DEFAULT_TTL)
    try:
        ttl = int(ttl)
    except (TypeError, ValueError):
        logger.warning("Invalid MESSAGE_STORAGE_TTL %r, using %s", ttl, DEFAULT_TTL)
        return DEFAULT_TTL
    if ttl <= 0:
        logger.warning("MESSAGE_STORAGE_TTL must be positive, using %s", DEFAULT_TTL)
        return DEFAULT_TTL
    return ttl


class CacheStorage(SessionStorage):
    """
    A storage backend for Django messages that uses Django's cache framework.
    """

    def _get(self, *args, **kwargs):
        """
        Retrieve messages from the cache.

        A cache backend problem is logged and treated as "no messages"
        rather than turned into a request-crashing exception.

        Returns:
            tuple: A tuple containing the list of messages and a boolean indicating if messages were retrieved.
        """
        if not self.request.session or not self.request.session.session_key:
            return [], False

        cache_key = f"{self.session_key}_{self.request.session.session_key}"
        cached_messages = cache.get(cache_key)

        if cached_messages is None:
            return [], False

        try:
            messages = self.deserialize_messages(cached_messages)
        except Exception:
            logger.warning(
                "Failed to deserialize cached messages for key %s", cache_key, exc_info=True
            )
            cache.delete(cache_key)
            return [], False
        return messages, True

    def _store(self, messages, response, *args, **kwargs):
        """
        Store messages in the cache.

        Args:
            messages: The messages to store.
            response: The response object.

        Returns:
            list: An empty list, as no messages are stored in the response.
        """
        if not self.request.session or not self.request.session.session_key:
            return []

        cache_key = f"{self.session_key}_{self.request.session.session_key}"

        if messages:
            try:
                serialized_messages = self.serialize_messages(messages)
            except Exception:
                logger.warning(
                    "Failed to serialize messages for key %s", cache_key, exc_info=True
                )
                cache.delete(cache_key)
                return []
            cache.set(cache_key, serialized_messages, _get_ttl())
        else:
            cache.delete(cache_key)
