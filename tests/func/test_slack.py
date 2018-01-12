import pytest


class TestSlackUserQuery():
    """Test slack user API queries"""

    @pytest.mark.django_db
    def test_get_slack_user(self, slack_user_factory, client):
        slack_user = slack_user_factory()


        query = {'query': f'{{ slackUser(id: "{slack_user.id}") {{ firstName }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['slackUser']['firstName'] == slack_user.first_name

    @pytest.mark.django_db
    def test_get_slack_users(self, slack_user_factory, client):
        slack_user = slack_user_factory()
        another_slack_user = slack_user_factory()

        query = {'query': '{ slackUsers { displayName } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['slackUsers']) == 2


class TestSlackTeamQuery():
    """Test slack team queries"""

    @pytest.mark.django_db
    def test_get_slack_team(self, slack_team_factory, client):
        slack_team = slack_team_factory()

        query = {'query': f'{{ slackTeam(id: "{slack_team.id}") {{ name }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['slackTeam']['name'] == slack_team.name

    @pytest.mark.django_db
    def test_get_slack_teams(self, slack_team_factory, client):
        slack_team = slack_team_factory()
        another_slack_team = slack_team_factory()

        query = {'query': '{ slackTeams { group { name } } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['slackTeams']) == 2


class TestSlackChannelQuery():
    """Test Slack Channel API queries"""
    @pytest.mark.django_db
    def test_get_slack_channel(self, slack_channel_factory, client):
        slack_channel = slack_channel_factory()

        query = {'query': f'{{ slackChannel(id: "{slack_channel.id}") {{ name }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['slackChannel']['name'] == slack_channel.name

    @pytest.mark.django_db
    def test_get_slack_channels(self, slack_channel_factory, client):
        slack_channel = slack_channel_factory()
        another_slack_channel = slack_channel_factory()

        query = {'query': '{ slackChannels { name } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['slackChannels']) == 2


class TestSlackSettingsQuery():
    """Test Slack Settings API queries"""
    @pytest.mark.django_db
    def test_get_slack_settings(self, slack_settings_factory, client):
        slack_settings = slack_settings_factory()

        query = {'query': f'{{ slackSettings(id: {slack_settings.id}) {{ botToken }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['slackSettings']['botToken'] == slack_settings.bot_token

    @pytest.mark.django_db
    def test_get_slacks_settings(self, slack_settings_factory, client):
        slack_settings = slack_settings_factory()
        another_slack_settings = slack_settings_factory()

        query = {'query': '{ slacksSettings { botToken } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['slacksSettings']) == 2
