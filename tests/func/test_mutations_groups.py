import pytest


class TestCreateGroup:

    @pytest.mark.django_db
    def test_create_group_unauthenticated(self, client, group_factory):
        group = group_factory.build()

        mutation = f'''
          mutation {{
            createGroup(input: {{name: "{group.name}"}}) {{
              group {{
                name
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createGroup'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_group(self, auth_client, group_factory):
        group = group_factory.build()

        mutation = f'''
          mutation {{
            createGroup(input: {{name: "{group.name}"}}) {{
              group {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createGroup']['group']['name'] == group.name


class TestCreateGroupSettings:

    @pytest.mark.django_db
    def test_create_group_setting_unauthenticated(self, client, group_factory, group_setting_factory):
        group = group_factory()
        group_setting = group_setting_factory.build(group=group)

        mutation = f'''
          mutation {{
            createGroupSetting(input: {{groupId: {group.id},
                                        name: "{group_setting.name}",
                                        value: "{group_setting.value}",
                                        dataType: "{group_setting.data_type}"}}) {{
              groupSetting {{
                name
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createGroupSetting'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_group_setting_invalid_group(self, auth_client, group_setting_factory):
        group_setting = group_setting_factory.build()

        mutation = f'''
          mutation {{
            createGroupSetting(input: {{groupId: 1,
                                        name: "{group_setting.name}",
                                        value: "{group_setting.value}",
                                        dataType: "{group_setting.data_type}" }}) {{
              groupSetting {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createGroupSetting'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Group Id'

    @pytest.mark.django_db
    def test_create_group_setting(self, auth_client, group_factory, group_setting_factory):
        group = group_factory()
        group_setting = group_setting_factory.build()

        mutation = f'''
          mutation {{
            createGroupSetting(input: {{groupId: {group.id},
                                        name: "{group_setting.name}",
                                        value: "{group_setting.value}",
                                        dataType: "{group_setting.data_type}"}}) {{
              groupSetting {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createGroupSetting']['groupSetting']['name'] == group_setting.name
