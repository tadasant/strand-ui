import pytest


class TestUpdateSlackApplicationInstallationHelpChannelAndActivate:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_application_installation_factory):
        slack_application_installation = slack_application_installation_factory(help_channel_id=None)
        help_channel_id = slack_application_installation_factory.build().help_channel_id

        mutation = f'''
          mutation {{
            updateSlackApplicationInstallationHelpChannelAndActivate(
              input: {{slackTeamId: "{slack_application_installation.slack_team_id}",
                       helpChannelId: "{help_channel_id}"}}) {{
              slackApplicationInstallation {{
                helpChannelId
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['updateSlackApplicationInstallationHelpChannelAndActivate'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_team(self, auth_client, slack_team_factory, slack_application_installation_factory):
        slack_team = slack_team_factory.build()
        slack_application_installation_factory(help_channel_id=None)
        help_channel_id = slack_application_installation_factory.build().help_channel_id

        mutation = f'''
          mutation {{
            updateSlackApplicationInstallationHelpChannelAndActivate(input: {{slackTeamId: "{slack_team.id}",
                                                                              helpChannelId: "{help_channel_id}"}}) {{
              slackApplicationInstallation {{
                helpChannelId
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})
        print(response.content)

        assert response.status_code == 200
        assert response.json()['data']['updateSlackApplicationInstallationHelpChannelAndActivate'] is None
        assert response.json()['errors'][0]['message'] == 'SlackApplicationInstallation matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, slack_application_installation_factory):
        slack_application_installation = slack_application_installation_factory(help_channel_id=None, is_active=False)
        help_channel_id = slack_application_installation_factory.build().help_channel_id

        mutation = f'''
          mutation {{
            updateSlackApplicationInstallationHelpChannelAndActivate(input: {{slackTeamId:
              "{slack_application_installation.slack_team_id}", helpChannelId: "{help_channel_id}"}}) {{
              slackApplicationInstallation {{
                helpChannelId
                isActive
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['updateSlackApplicationInstallationHelpChannelAndActivate'][
                   'slackApplicationInstallation']['helpChannelId'] == help_channel_id
        assert response.json()['data']['updateSlackApplicationInstallationHelpChannelAndActivate'][
            'slackApplicationInstallation']['isActive']
