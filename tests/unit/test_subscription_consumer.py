import pytz
from datetime import datetime, timedelta

import pytest

from app.topics.models import Discussion
from tests.utils import wait_until


class TestSubscriptionConsumer:
    @pytest.mark.asyncio
    async def test_invalid_message_type(self, communicator):
        response = await communicator.receive_from()
        assert response == '{"type": "connection_ack"}'

        await communicator.send_to(text_data='{"type": "hello"}')
        response = await communicator.receive_from()

        assert response == '{"type": "error", "payload": {"errors": [{"message": "Unknown message type"}]}}'

    @pytest.mark.asyncio
    async def test_invalid_subscription(self, communicator):
        response = await communicator.receive_from()
        assert response == '{"type": "connection_ack"}'

        await communicator.send_to(text_data='{"type": "start", "payload": {"query": "autoClosedTopics"}}')
        response = await communicator.receive_from()

        assert response == '{"type": "error", "payload": {"errors": [{"message": "Unknown subscription"}]}}'

    @pytest.mark.asyncio
    async def test_subscribe_to_stale_discussion(self, mark_stale_discussions_factory, discussion_factory,
    communicator, slack_channel_factory, event_loop):
        response = await communicator.receive_from()
        assert response == '{"type": "connection_ack"}'

        mark_stale_discussions_factory(num_periods=3, period_length=1.5)
        await communicator.send_to(text_data='{"type": "start", "payload": {"query": "autoClosedDiscussion"}}')

        discussion = discussion_factory(time_start=datetime.now(pytz.UTC) - timedelta(minutes=30))
        slack_channel_factory(discussion=discussion)

        wait_until(condition=lambda: Discussion.objects.get(pk=discussion.id).is_stale, timeout=5)

        response = await communicator.receive_from(timeout=3)
        assert response == f'{{"type": "data", "payload": {{"id": {discussion.id}}}}}'
