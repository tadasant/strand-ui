import pytest


class TestCreateGroup:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, group_factory):
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
    def test_valid(self, auth_client, group_factory):
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
