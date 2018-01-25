import pytest


class TestQuerySlackChannels:

    @pytest.mark.django_db
    def test_get_slack_channel(self, slack_channel_factory, client):
        slack_channel = slack_channel_factory()

        query = {'query': f'{{ slackChannel(id: "{slack_channel.id}") {{ name }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['slackChannel']['name'] == slack_channel.name

    @pytest.mark.django_db
    def test_get_slack_channels(self, slack_channel_factory, client):
        slack_channel_factory()
        slack_channel_factory()

        query = {'query': '{ slackChannels { name } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['slackChannels']) == 2
