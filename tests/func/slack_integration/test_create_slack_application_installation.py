import pytest


class TestCreateSlackApplicationInstallation:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_team_factory, slack_user_factory,
                             slack_application_installation_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory()
        slack_application_installation = slack_application_installation_factory.build(slack_team=slack_team,
                                                                                      installer=slack_user)

        mutation = f'''
          mutation {{
            createSlackApplicationInstallation(input: {{slackTeamId: "{slack_team.id}",
                                                        accessToken: "{slack_application_installation.access_token}",
                                                        scope: "{slack_application_installation.scope}",
                                                        installerId: "{slack_application_installation.installer.id}",
                                                        botUserId: "{slack_application_installation.bot_user_id}",
                                                        botAccessToken:
                                                        "{slack_application_installation.bot_access_token}"}}) {{
              slackApplicationInstallation {{
                accessToken
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackApplicationInstallation'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_team(self, auth_client, slack_team_factory, slack_user_factory,
                          slack_application_installation_factory):
        slack_team = slack_team_factory.build()
        slack_user = slack_user_factory()
        slack_application_installation = slack_application_installation_factory.build(slack_team=slack_team,
                                                                                      installer=slack_user)

        mutation = f'''
          mutation {{
            createSlackApplicationInstallation(input: {{slackTeamId: "{slack_team.id}",
                                                        accessToken: "{slack_application_installation.access_token}",
                                                        scope: "{slack_application_installation.scope}",
                                                        installerId: "{slack_application_installation.installer.id}",
                                                        botUserId: "{slack_application_installation.bot_user_id}",
                                                        botAccessToken:
                                                        "{slack_application_installation.bot_access_token}"}}) {{
              slackApplicationInstallation {{
                accessToken
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        print(response.content)
        assert response.status_code == 200
        assert response.json()['data']['createSlackApplicationInstallation'] is None
        assert response.json()['errors'][0]['message'] == f"{{'slack_team_id': ['Invalid pk \"{slack_team.id}\" - " \
                                                          "object does not exist.']}"

    @pytest.mark.django_db
    def test_valid(self, auth_client, slack_team_factory, slack_user_factory, slack_application_installation_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory()
        slack_application_installation = slack_application_installation_factory.build(slack_team=slack_team,
                                                                                      installer=slack_user)

        mutation = f'''
          mutation {{
            createSlackApplicationInstallation(input: {{slackTeamId: "{slack_team.id}",
                                                        accessToken: "{slack_application_installation.access_token}",
                                                        scope: "{slack_application_installation.scope}",
                                                        installerId: "{slack_application_installation.installer.id}",
                                                        botUserId: "{slack_application_installation.bot_user_id}",
                                                        botAccessToken:
                                                        "{slack_application_installation.bot_access_token}"}}) {{
              slackApplicationInstallation {{
                accessToken
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackApplicationInstallation']['slackApplicationInstallation'][
                   'accessToken'] == slack_application_installation.access_token
