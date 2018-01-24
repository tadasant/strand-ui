import pytest


class TestQueryUsers:

    @pytest.mark.django_db
    def test_get_user(self, user_factory, client):
        user = user_factory()

        query = {'query': f'{{ user(id: {user.id}) {{ firstName }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['user']['firstName'] == user.first_name

    @pytest.mark.django_db
    def test_get_users(self, user_factory, client):
        user_factory()
        user_factory()

        query = {'query': '{ users { username } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['users']) == 2
