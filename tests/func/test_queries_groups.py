import pytest


class TestQueryGroups:

    @pytest.mark.django_db
    def test_get_group(self, group_factory, client):
        group = group_factory()

        query = {'query': f'{{ group(name: "{group.name}") {{ id }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['group']['id'] == str(group.id)

    @pytest.mark.django_db
    def test_get_groups(self, group_factory, client):
        group = group_factory()
        another_group = group_factory()

        query = {'query': '{ groups { name } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['groups']) == 2


class TestQueryGroupSettings:

    @pytest.mark.django_db
    def test_get_group_settings(self, group_settings_factory, client):
        group_settings = group_settings_factory()

        query = {'query': f'{{ groupSettings(id: {group_settings.id}) {{ isPublic }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['groupSettings']['isPublic'] == group_settings.is_public

    @pytest.mark.django_db
    def test_get_groups(self, group_settings_factory, client):
        group_settings = group_settings_factory()
        another_group_settings = group_settings_factory()

        query = {'query': '{ groupsSettings { group { name } } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['groupsSettings']) == 2