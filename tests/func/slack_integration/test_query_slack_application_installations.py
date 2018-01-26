import pytest


class TestQuerySlackApplicationInstallations:

    @pytest.mark.django_db
    def test_get_slack_application_installation(self, slack_application_installation_factory, auth_client):
        slack_application_installation = slack_application_installation_factory()

        query = {'query': f'{{ slackApplicationInstallation(id: {slack_application_installation.id}) '
                          f'{{ botAccessToken }} }}'}
        response = auth_client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['slackApplicationInstallation']['botAccessToken'] == \
            slack_application_installation.bot_access_token

    @pytest.mark.django_db
    def test_get_slack_application_installations(self, slack_application_installation_factory, auth_client):
        slack_application_installation_factory()
        slack_application_installation_factory()

        query = {'query': '{ slackApplicationInstallations { botAccessToken } }'}
        response = auth_client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['slackApplicationInstallations']) == 2
