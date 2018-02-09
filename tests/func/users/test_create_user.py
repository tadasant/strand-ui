import pytest


class TestCreateUser:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, user_factory):
        user = user_factory.build()
        mutation = f'''
          mutation {{
            createUser(input: {{email: "{user.email}", username: "{user.username}"}}) {{
              user {{
                alias
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUser'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, user_factory):
        user = user_factory.build()

        mutation = f'''
          mutation {{
            createUser(input: {{email: "{user.email}", username: "{user.username}"}}) {{
              user {{
                alias
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUser']['user']['alias']
