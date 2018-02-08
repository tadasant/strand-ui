import pytest


class TestSubscriptionConsumer:
    @pytest.mark.asyncio
    async def test_send_message(self, websocket_communicator):
        await websocket_communicator.send_to(text_data='hello')
        response = await websocket_communicator.receive_from()
        assert response
