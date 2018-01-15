import pytest


class TestGroupMutations():
    """Test group mutations"""

    @pytest.mark.django_db
    def test_create_group_unauthenticated(self, client):
        mutation = f'''
          mutation {{
            createGroup(input: {{name: "mygroup"}}) {{
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
    def test_create_group(self, auth_client):
        mutation = f'''
          mutation {{
            createGroup(input: {{name: "mygroup"}}) {{
              group {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createGroup']['group']['name'] == 'mygroup'


class TestGroupSettingsMutations():
    """Test group settings mutations"""

    @pytest.mark.django_db
    def test_create_group_settings_unauthenticated(self, client, group_factory):
        group = group_factory()

        mutation = f'''
          mutation {{
            createGroupSettings(input: {{groupId: {group.id}, isPublic: true}}) {{
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
    def test_create_group_settings_invalid_group(self, auth_client):
        mutation = f'''
          mutation {{
            createGroupSettings(input: {{groupId: 1, isPublic: true}}) {{
              groupSettings {{
                isPublic
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createGroupSettings'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Group Id'

    @pytest.mark.django_db
    def test_create_group_settings(self, auth_client, group_factory):
        group = group_factory()

        mutation = f'''
          mutation {{
            createGroupSettings(input: {{groupId: {group.id}, isPublic: true}}) {{
              groupSettings {{
                isPublic
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createGroupSettings']['groupSettings']['isPublic']
