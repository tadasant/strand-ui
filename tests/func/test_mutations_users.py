import pytest


class TestUserMutations():
    """Test user mutations"""

    @pytest.mark.django_db
    def test_create_user_unauthenticated(self, client):
        mutation = f'''
          mutation {{
            createUser(input: {{email: "frodo@gmail.com", username: "frodo"}}) {{
              user {{
                username
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUser'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_user(self, auth_client):
        mutation = f'''
          mutation {{
            createUser(input: {{email: "frodo@gmail.com", username: "frodo"}}) {{
              user {{
                username
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUser']['user']['username'] == 'frodo'
