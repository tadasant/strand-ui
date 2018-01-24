import pytest


class TestQuerySlackTeamInstallations:

    @pytest.mark.django_db
    def test_get_slack_team_installation(self, slack_team_installation_factory, client):
        slack_team_installation = slack_team_installation_factory()

        query = {'query': f'{{ slackTeamInstallation(id: {slack_team_installation.id}) {{ botAccessToken }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['slackTeamInstallation']['botAccessToken'] == \
            slack_team_installation.bot_access_token

    @pytest.mark.django_db
    def test_get_slack_team_installations(self, slack_team_installation_factory, client):
        slack_team_installation_factory()
        slack_team_installation_factory()

        query = {'query': '{ slackTeamInstallations { botAccessToken } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['slackTeamInstallations']) == 2
