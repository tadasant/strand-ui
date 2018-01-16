import pytest


class TestQueryQuestions:
    """Test question API queries"""

    @pytest.mark.django_db
    def test_get_question(self, question_factory, client):
        question = question_factory()

        query = {'query': f'{{ question(id: {question.id}) {{ title }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['question']['title'] == question.title

    @pytest.mark.django_db
    def test_get_questions(self, question_factory, client):
        question_factory()
        question_factory()

        query = {'query': '{ questions { title } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['questions']) == 2


class TestQueryTags:

    @pytest.mark.django_db
    def test_get_tag(self, tag_factory, client):
        tag = tag_factory()

        query = {'query': f'{{ tag(name: "{tag.name}") {{ id }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['tag']['id'] == str(tag.id)

    @pytest.mark.django_db
    def test_get_tags(self, tag_factory, client):
        tag_factory()
        tag_factory()

        query = {'query': '{ tags { name } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['tags']) == 2


class TestQuerySessions:
    """Test session API queries"""

    @pytest.mark.django_db
    def test_get_session(self, session_factory, client):
        session = session_factory()

        query = {'query': f'{{ session(id: {session.id}) {{ question {{ title }} }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['session']['question']['title'] == session.question.title

    @pytest.mark.django_db
    def test_get_sessions(self, session_factory, client):
        session_factory()
        session_factory()

        query = {'query': '{ sessions { id } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['sessions']) == 2
