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
    def test_create_group_settings_unauthenticated(self, client, group_factory, group_settings_factory):
        group = group_factory()
        group_settings = group_settings_factory.build()

        mutation = f'''
          mutation {{
            createGroupSettings(input: {{groupId: {group.id}, isPublic: {str(group_settings.is_public).lower()}}}) {{
              groupSettings {{
                isPublic
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createGroupSettings'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_group_settings_invalid_group(self, auth_client, group_settings_factory):
        group_settings = group_settings_factory.build()

        mutation = f'''
          mutation {{
            createGroupSettings(input: {{groupId: 1, isPublic: {str(group_settings.is_public).lower()}}}) {{
              groupSettings {{
                isPublic
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        print(response.content)

        assert response.status_code == 200
        assert response.json()['data']['createGroupSettings'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Group Id'

    @pytest.mark.django_db
    def test_create_group_settings(self, auth_client, group_factory, group_settings_factory):
        group = group_factory()
        group_settings = group_settings_factory.build()

        mutation = f'''
          mutation {{
            createGroupSettings(input: {{groupId: {group.id}, isPublic: {str(group_settings.is_public).lower()}}}) {{
              groupSettings {{
                isPublic
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createGroupSettings']['groupSettings']['isPublic'] == group_settings.is_public
