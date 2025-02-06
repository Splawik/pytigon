from pytigon.schserw.routing import *

# Pytest tests
import pytest
from channels.testing import WebsocketCommunicator


@pytest.mark.asyncio
async def test_lifespan_app():
    """Test LifespanApp handling of lifespan events."""
    app = LifespanApp({"type": "lifespan"})

    async def receive():
        return {"type": "lifespan.startup"}

    async def send(message):
        assert message == {"type": "lifespan.startup.complete"}

    await app(None, send)

    async def receive_shutdown():
        return {"type": "lifespan.shutdown"}

    async def send_shutdown(message):
        assert message == {"type": "lifespan.shutdown.complete"}

    await app(receive_shutdown, send_shutdown)


@pytest.mark.asyncio
async def test_websocket_connection():
    """Test WebSocket connection routing."""
    communicator = WebsocketCommunicator(application, "/test/")
    connected, _ = await communicator.connect()
    assert connected
    await communicator.disconnect()
