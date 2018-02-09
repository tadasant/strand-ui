import pytest


class TestQueryUsers:

    @pytest.mark.django_db
    def test_get_user_unauthorized_fields(self, user_factory, client):
        user = user_factory()

        query = {'query': f'{{ user(id: {user.id}) {{ slackUsers {{ id }} }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert not response.json()['data']['user']['slackUsers']
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_get_user_public_fields(self, user_factory, client):
        user = user_factory()

        query = {'query': f'{{ user(id: {user.id}) {{ alias }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['user']['alias'] == user.alias

    @pytest.mark.django_db
    def test_get_users_authorized_fields(self, user_factory, auth_client):
        user_factory()
        user_factory()

        query = {'query': '{ users { slackUsers { id } } }'}
        response = auth_client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['users']) == 3
