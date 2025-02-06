from django.contrib.messages.storage.session import SessionStorage
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured


class CacheStorage(SessionStorage):
    """
    A storage backend for Django messages that uses Django's cache framework.
    """

    def _get(self, *args, **kwargs):
        """
        Retrieve messages from the cache.

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
            return messages, True
        except Exception as e:
            raise ImproperlyConfigured(f"Failed to deserialize messages: {e}")

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
            return

        cache_key = f"{self.session_key}_{self.request.session.session_key}"

        if messages:
            try:
                serialized_messages = self.serialize_messages(messages)
                cache.set(cache_key, serialized_messages)
            except Exception as e:
                raise ImproperlyConfigured(f"Failed to serialize messages: {e}")
        else:
            cache.delete(cache_key)
