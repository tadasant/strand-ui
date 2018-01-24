import pytest


class TestQueryMessages:

    @pytest.mark.django_db
    def test_get_message(self, message_factory, client):
        message = message_factory()

        query = {'query': f'{{ message(id: {message.id}) {{ text }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['message']['text'] == message.text

    @pytest.mark.django_db
    def test_get_messages(self, message_factory, client):
        message_factory()
        message_factory()

        query = {'query': '{ messages { text } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['messages']) == 2
