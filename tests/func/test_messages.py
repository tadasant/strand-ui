import pytest


class TestMessageQuery():
    """Test message API queries"""

    @pytest.mark.django_db
    def test_get_message(self, message_factory, client):
        message = message_factory()

        query = {'query': f'{{ message(id: {message.id}) {{ text }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['message']['text'] == message.text

    @pytest.mark.django_db
    def test_get_messages(self, message_factory, client):
        message = message_factory()
        another_message = message_factory()

        query = {'query': '{ messages { text } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['messages']) == 2


class TestReplyQuery():
    """Test reply API queries"""

    @pytest.mark.django_db
    def test_get_reply(self, reply_factory, client):
        reply = reply_factory()

        query = {'query': f'{{ reply(id: {reply.id}) {{ message {{ text }} }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['reply']['message']['text'] == reply.message.text

    @pytest.mark.django_db
    def test_get_replies(self, reply_factory, client):
        reply = reply_factory()
        another_reply = reply_factory(message=reply.message)

        query = {'query': '{ replies { text } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['replies']) == 2