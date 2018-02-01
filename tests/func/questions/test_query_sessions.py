import pytest


class TestQuerySessions:

    @pytest.mark.django_db
    def test_get_session(self, session_factory, client):
        session = session_factory()

        query = {'query': f'{{ session(id: {session.id}) {{ topic {{ title }} }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['session']['topic']['title'] == session.topic.title

    @pytest.mark.django_db
    def test_get_sessions(self, session_factory, client):
        session_factory()
        session_factory()

        query = {'query': '{ sessions { id } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['sessions']) == 2
