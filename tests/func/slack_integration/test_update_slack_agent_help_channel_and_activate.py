import pytest


class TestUpdateSlackAgentHelpChannelAndActivate:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_agent_factory, slack_team_factory):
        slack_agent = slack_agent_factory(help_channel_id=None)
        slack_team = slack_team_factory(slack_agent=slack_agent)
        help_channel_id = slack_agent_factory.build().help_channel_id

        mutation = f'''
          mutation {{
            updateSlackAgentHelpChannelAndActivate(input: {{slackTeamId: "{slack_team.id}",
                                                            helpChannelId: "{help_channel_id}"}}) {{
              slackAgent {{
                helpChannelId
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['updateSlackAgentHelpChannelAndActivate'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_team(self, auth_client, slack_agent_factory, slack_team_factory):
        slack_agent = slack_agent_factory(help_channel_id=None)
        slack_team = slack_team_factory.build(slack_agent=slack_agent)
        help_channel_id = slack_agent_factory.build().help_channel_id

        mutation = f'''
          mutation {{
            updateSlackAgentHelpChannelAndActivate(input: {{slackTeamId: "{slack_team.id}",
                                                            helpChannelId: "{help_channel_id}"}}) {{
              slackAgent {{
                helpChannelId
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['updateSlackAgentHelpChannelAndActivate'] is None
        assert response.json()['errors'][0]['message'] == 'SlackAgent matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, slack_agent_factory, slack_team_factory):
        slack_agent = slack_agent_factory(help_channel_id=None)
        slack_team = slack_team_factory(slack_agent=slack_agent)
        help_channel_id = slack_agent_factory.build().help_channel_id

        mutation = f'''
          mutation {{
            updateSlackAgentHelpChannelAndActivate(input: {{slackTeamId: "{slack_team.id}",
                                                            helpChannelId: "{help_channel_id}"}}) {{
              slackAgent {{
                helpChannelId
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['updateSlackAgentHelpChannelAndActivate']['slackAgent']['helpChannelId'] == \
               help_channel_id
        assert response.json()['data']['updateSlackAgentHelpChannelAndActivate']['slackAgent']['status'] == 'ACTIVE'
