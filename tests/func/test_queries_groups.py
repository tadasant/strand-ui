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
        group_factory()
        group_factory()

        query = {'query': '{ groups { name } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['groups']) == 2


class TestQueryGroupSettings:

    @pytest.mark.django_db
    def test_get_group_setting(self, group_setting_factory, client):
        group_setting = group_setting_factory()

        query = {'query': f'{{ groupSetting(id: {group_setting.id}) {{ name }} }}'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert response.json()['data']['groupSetting']['name'] == group_setting.name

    @pytest.mark.django_db
    def test_get_groups(self, group_setting_factory, client):
        group_setting_factory()
        group_setting_factory()

        query = {'query': '{ groupSettings { group { id } } }'}
        response = client.post('/graphql', query)

        assert response.status_code == 200
        assert len(response.json()['data']['groupSettings']) == 2
