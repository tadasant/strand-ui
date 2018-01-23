import pytest


class TestCreateSlackTeamInstallation:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_team_factory, slack_user_factory,
                             slack_team_installation_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory()
        slack_team_installation = slack_team_installation_factory.build(slack_team=slack_team, installer=slack_user)

        mutation = f'''
          mutation {{
            createSlackTeamInstallation(input: {{slackTeamId: "{slack_team.id}",
                                                 accessToken: "{slack_team_installation.access_token}",
                                                 scope: "{slack_team_installation.scope}",
                                                 installerId: "{slack_team_installation.installer.id}",
                                                 botUserId: "{slack_team_installation.bot_user_id}",
                                                 botAccessToken: "{slack_team_installation.bot_access_token}"}}) {{
              slackTeamInstallation {{
                accessToken
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackTeamInstallation'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_team(self, auth_client, slack_team_factory, slack_user_factory, slack_team_installation_factory):
        slack_team = slack_team_factory.build()
        slack_user = slack_user_factory()
        slack_team_installation = slack_team_installation_factory.build(slack_team=slack_team, installer=slack_user)

        mutation = f'''
          mutation {{
            createSlackTeamInstallation(input: {{slackTeamId: "{slack_team.id}",
                                                 accessToken: "{slack_team_installation.access_token}",
                                                 scope: "{slack_team_installation.scope}",
                                                 installerId: "{slack_team_installation.installer.id}",
                                                 botUserId: "{slack_team_installation.bot_user_id}",
                                                 botAccessToken: "{slack_team_installation.bot_access_token}"}}) {{
              slackTeamInstallation {{
                accessToken
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackTeamInstallation'] is None
        assert response.json()['errors'][0]['message'] == 'Invalid Slack Team Id'

    @pytest.mark.django_db
    def test_valid(self, auth_client, slack_team_factory, slack_user_factory, slack_team_installation_factory):
        slack_team = slack_team_factory()
        slack_user = slack_user_factory()
        slack_team_installation = slack_team_installation_factory.build(slack_team=slack_team, installer=slack_user)

        mutation = f'''
          mutation {{
            createSlackTeamInstallation(input: {{slackTeamId: "{slack_team.id}",
                                                 accessToken: "{slack_team_installation.access_token}",
                                                 scope: "{slack_team_installation.scope}",
                                                 installerId: "{slack_team_installation.installer.id}",
                                                 botUserId: "{slack_team_installation.bot_user_id}",
                                                 botAccessToken: "{slack_team_installation.bot_access_token}"}}) {{
              slackTeamInstallation {{
                accessToken
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackTeamInstallation']['slackTeamInstallation']['accessToken'] ==\
            slack_team_installation.access_token
