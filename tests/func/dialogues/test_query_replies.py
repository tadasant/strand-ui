import pytest


class TestQueryReplies:

    @pytest.mark.django_db
    def test_get_reply(self, reply_factory, client):
        reply = reply_factory()

        query = {'query': f'{{ reply(id: {reply.id}) {{ message {{ text }} }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['reply']['message']['text'] == reply.message.text

    @pytest.mark.django_db
    def test_get_replies(self, reply_factory, client):
        reply_factory()
        reply_factory()

        query = {'query': '{ replies { text } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['replies']) == 2
