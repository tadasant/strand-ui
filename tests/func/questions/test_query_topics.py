import pytest


class TestQueryTopics:

    @pytest.mark.django_db
    def test_get_topic(self, topic_factory, client):
        topic = topic_factory()

        query = {'query': f'{{ topic(id: {topic.id}) {{ title }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['topic']['title'] == topic.title

    @pytest.mark.django_db
    def test_get_topics(self, topic_factory, client):
        topic_factory()
        topic_factory()

        query = {'query': '{ topics { title } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['topics']) == 2
