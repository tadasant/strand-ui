import pytest


class TestCreateUserFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_team_factory, slack_user_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team)

        mutation = f'''
          mutation {{
            createUserFromSlack(input: {{id: "{slack_user.id}",
                                         name: "{slack_user.name}",
                                         firstName: "{slack_user.first_name}",
                                         lastName: "{slack_user.last_name}",
                                         realName: "{slack_user.real_name}",
                                         displayName: "{slack_user.display_name}",
                                         email: "{slack_user.email}",
                                         avatar72: "{slack_user.avatar_72}",
                                         isBot: {str(slack_user.is_bot).lower()},
                                         isAdmin: {str(slack_user.is_admin).lower()},
                                         slackTeamId: "{slack_team.id}"}}) {{
              slackUser {{
                user {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_existing_slack_user(self, auth_client, slack_team_factory, slack_user_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory(slack_team=slack_team)

        mutation = f'''
          mutation {{
            createUserFromSlack(input: {{id: "{slack_user.id}",
                                         name: "{slack_user.name}",
                                         firstName: "{slack_user.first_name}",
                                         lastName: "{slack_user.last_name}",
                                         realName: "{slack_user.real_name}",
                                         displayName: "{slack_user.display_name}",
                                         email: "{slack_user.email}",
                                         avatar72: "{slack_user.avatar_72}",
                                         isBot: {str(slack_user.is_bot).lower()},
                                         isAdmin: {str(slack_user.is_admin).lower()},
                                         slackTeamId: "{slack_team.id}"}}) {{
              slackUser {{
                user {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserFromSlack'] is None
        assert response.json()['errors'][0]['message'] == "{'id': ['slack user with this id already exists.']}"

    @pytest.mark.django_db
    def test_valid_and_gets_user(self, auth_client, slack_team_factory, user_factory, slack_user_factory):
        slack_team = slack_team_factory()
        user = user_factory()
        slack_user = slack_user_factory.build(slack_team=slack_team, email=user.email)

        mutation = f'''
          mutation {{
            createUserFromSlack(input: {{id: "{slack_user.id}",
                                         name: "{slack_user.name}",
                                         firstName: "{slack_user.first_name}",
                                         lastName: "{slack_user.last_name}",
                                         realName: "{slack_user.real_name}",
                                         displayName: "{slack_user.display_name}",
                                         email: "{slack_user.email}",
                                         avatar72: "{slack_user.avatar_72}",
                                         isBot: {str(slack_user.is_bot).lower()},
                                         isAdmin: {str(slack_user.is_admin).lower()},
                                         slackTeamId: "{slack_team.id}"}}) {{
              slackUser {{
                user {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserFromSlack']['slackUser']['user']['id'] == str(user.id)

    @pytest.mark.django_db
    def test_valid_and_creates_user(self, auth_client, slack_team_factory, user_factory, slack_user_factory):
        slack_team = slack_team_factory()
        user = user_factory.build()
        slack_user = slack_user_factory.build(slack_team=slack_team, email=user.email)

        mutation = f'''
          mutation {{
            createUserFromSlack(input: {{id: "{slack_user.id}",
                                         name: "{slack_user.name}",
                                         firstName: "{slack_user.first_name}",
                                         lastName: "{slack_user.last_name}",
                                         realName: "{slack_user.real_name}",
                                         displayName: "{slack_user.display_name}",
                                         email: "{slack_user.email}",
                                         avatar72: "{slack_user.avatar_72}",
                                         isBot: {str(slack_user.is_bot).lower()},
                                         isAdmin: {str(slack_user.is_admin).lower()},
                                         slackTeamId: "{slack_team.id}"}}) {{
              slackUser {{
                user {{
                  email
                  isBot
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createUserFromSlack']['slackUser']['user']['email'] == slack_user.email
        assert response.json()['data']['createUserFromSlack']['slackUser']['user']['isBot'] == slack_user.is_bot
