import pytest


class TestQuerySlackTeams:

    @pytest.mark.django_db
    def test_get_slack_team(self, slack_team_factory, client):
        slack_team = slack_team_factory()

        query = {'query': f'{{ slackTeam(id: "{slack_team.id}") {{ name }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['slackTeam']['name'] == slack_team.name

    @pytest.mark.django_db
    def test_get_slack_teams(self, slack_team_factory, client):
        slack_team_factory()
        slack_team_factory()

        query = {'query': '{ slackTeams { group { name } } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['slackTeams']) == 2
