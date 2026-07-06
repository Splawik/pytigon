import asyncio
import contextlib

# Pytest tests
import pytest

from pytigon.schserw.routing import LifespanApp, application


def test_lifespan_app_startup():
    """Test LifespanApp handling of lifespan startup event."""

    async def _run():
        app = LifespanApp({"type": "lifespan"})
        received_messages = []

        async def receive():
            if not received_messages:
                return {"type": "lifespan.startup"}
            return {"type": "lifespan.shutdown"}

        async def send(message):
            received_messages.append(message)
            if message["type"] == "lifespan.shutdown.complete":
                raise StopAsyncIteration()

        with contextlib.suppress(StopAsyncIteration):
            await app(receive, send)

        return received_messages

    received_messages = asyncio.run(_run())
    assert len(received_messages) == 2
    assert received_messages[0] == {"type": "lifespan.startup.complete"}
    assert received_messages[1] == {"type": "lifespan.shutdown.complete"}


def test_lifespan_app_scoped():
    """Test LifespanApp with a scoped receive/send."""

    async def _run():
        app = LifespanApp({"type": "lifespan"})
        received_messages = []
        call_count = 0

        async def receive():
            nonlocal call_count
            call_count += 1
            if call_count == 1:
                return {"type": "lifespan.startup"}
            return {"type": "lifespan.shutdown"}

        async def send(message):
            received_messages.append(message)
            if message["type"] == "lifespan.shutdown.complete":
                raise StopAsyncIteration()

        with contextlib.suppress(StopAsyncIteration):
            await app(receive, send)

        return received_messages

    received_messages = asyncio.run(_run())
    assert len(received_messages) == 2
    assert received_messages[0] == {"type": "lifespan.startup.complete"}
    assert received_messages[1] == {"type": "lifespan.shutdown.complete"}
