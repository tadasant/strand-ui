import pytest


class TestQuerySlackUsers:

    @pytest.mark.django_db
    def test_get_slack_user_unauthorized(self, slack_user_factory, client):
        slack_user = slack_user_factory()

        query = f'''{{
          slackUser(id: "{slack_user.id}") {{
            displayName
            id
          }}
        }}'''
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_get_slack_user(self, slack_user_factory, auth_client):
        slack_user = slack_user_factory()

        query = f'''{{
          slackUser(id: "{slack_user.id}") {{
            id
            displayName
            slackTeam {{
              name
            }}
            user {{
              id
            }}
          }}
        }}'''
        response = auth_client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert response.json()['data']['slackUser']['displayName'] == slack_user.display_name

    @pytest.mark.django_db
    def test_get_slack_users_unauthorized(self, slack_user_factory, client):
        slack_user_factory()
        slack_user_factory()

        query = '''{
          slackUsers {
            id
          }
        }'''
        response = client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_get_slack_users(self, slack_user_factory, auth_client):
        slack_user_factory()
        slack_user_factory()

        query = '''{
          slackUsers {
            user {
              id
            }
          }
        }'''
        response = auth_client.post('/graphql', {'query': query})

        assert response.status_code == 200
        assert len(response.json()['data']['slackUsers']) == 2
