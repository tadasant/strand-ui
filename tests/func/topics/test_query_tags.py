import pytest


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
