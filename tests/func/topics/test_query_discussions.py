import pytest


class TestQueryDiscussions:

    @pytest.mark.django_db
    def test_get_discussion(self, discussion_factory, client):
        discussion = discussion_factory()

        query = {'query': f'{{ discussion(id: {discussion.id}) {{ topic {{ title }} }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['discussion']['topic']['title'] == discussion.topic.title

    @pytest.mark.django_db
    def test_get_discussions(self, discussion_factory, client):
        discussion_factory()
        discussion_factory()

        query = {'query': '{ discussions { id } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['discussions']) == 2
