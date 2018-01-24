import pytest


class TestCreateSlackUser:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, user_factory, slack_team_factory, slack_user_factory):
        user = user_factory()
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build()

        mutation = f'''
          mutation {{
            createSlackUser(input: {{id: "{slack_user.id}", name: "{slack_user.name}",
                                     realName: "{slack_user.real_name}", displayName: "{slack_user.display_name}",
                                     isBot: {str(slack_user.is_bot).lower()},
                                     isAdmin: {str(slack_user.is_admin).lower()}, slackTeamId: "{slack_team.id}",
                                     userId: {user.id}}}) {{
              slackUser {{
                realName
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_team(self, auth_client, user_factory, slack_team_factory, slack_user_factory):
        user = user_factory()
        slack_team = slack_team_factory.build()
        slack_user = slack_user_factory.build()

        mutation = f'''
          mutation {{
            createSlackUser(input: {{id: "{slack_user.id}", name: "{slack_user.name}",
                                     realName: "{slack_user.real_name}", displayName: "{slack_user.display_name}",
                                     isBot: {str(slack_user.is_bot).lower()},
                                     isAdmin: {str(slack_user.is_admin).lower()}, slackTeamId: "{slack_team.id}",
                                     userId: {user.id}}}) {{
              slackUser {{
                realName
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Team Id'

    @pytest.mark.django_db
    def test_invalid_user(self, auth_client, slack_team_factory, slack_user_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory()

        mutation = f'''
          mutation {{
            createSlackUser(input: {{id: "{slack_user.id}", name: "{slack_user.name}",
                                     realName: "{slack_user.real_name}", displayName: "{slack_user.display_name}",
                                     isBot: {str(slack_user.is_bot).lower()},
                                     isAdmin: {str(slack_user.is_admin).lower()}, slackTeamId: "{slack_team.id}",
                                     userId: 1}}) {{
              slackUser {{
                realName
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['errors'][0]['message'] == 'Invalid User Id'

    @pytest.mark.django_db
    def test_valid(self, auth_client, user_factory, slack_team_factory, slack_user_factory):
        user = user_factory()
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build()

        mutation = f'''
          mutation {{
            createSlackUser(input: {{id: "{slack_user.id}", name: "{slack_user.name}",
                                     realName: "{slack_user.real_name}", displayName: "{slack_user.display_name}",
                                     isBot: {str(slack_user.is_bot).lower()},
                                     isAdmin: {str(slack_user.is_admin).lower()}, slackTeamId: "{slack_team.id}",
                                     userId: {user.id}}}) {{
              slackUser {{
                realName
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackUser']['slackUser']['realName'] == slack_user.real_name
