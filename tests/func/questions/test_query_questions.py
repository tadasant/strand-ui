import pytest


class TestQueryQuestions:

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
