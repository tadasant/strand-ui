import pytest


class TestQuerySlackUsers:

    @pytest.mark.django_db
    def test_get_slack_user(self, slack_user_factory, client):
        slack_user = slack_user_factory()

        query = {'query': f'{{ slackUser(id: "{slack_user.id}") {{ firstName }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['slackUser']['firstName'] == slack_user.first_name

    @pytest.mark.django_db
    def test_get_slack_users(self, slack_user_factory, client):
        slack_user_factory()
        slack_user_factory()

        query = {'query': '{ slackUsers { displayName } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['slackUsers']) == 2
