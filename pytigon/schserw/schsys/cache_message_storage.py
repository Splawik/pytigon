from django.contrib.messages.storage.session import SessionStorage
from django.core.cache import cache


class CacheStorage(SessionStorage):
    def _get(self, *args, **kwargs):
        if self.request.session and self.request.session.session_key:
            ret = (
                self.deserialize_messages(
                    cache.get(self.session_key + "_" + self.request.session.session_key)
                ),
                True,
            )
            return ret
        else:
            return [], False

    def _store(self, messages, response, *args, **kwargs):
        if self.request.session and self.request.session.session_key:
            if messages:
                cache.set(
                    self.session_key + "_" + self.request.session.session_key,
                    self.serialize_messages(messages),
                )
            else:
                cache.delete(self.session_key + "_" + self.request.session.session_key)
        return []
