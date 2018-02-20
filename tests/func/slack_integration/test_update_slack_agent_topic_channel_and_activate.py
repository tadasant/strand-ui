import pytest


class TestUpdateSlackAgentTopicChannelAndActivate:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_agent_factory, slack_team_factory,
                             slack_application_installation_factory, slack_app_request_factory):
        slack_agent = slack_agent_factory(topic_channel_id=None)
        slack_application_installation_factory(slack_agent=slack_agent)
        slack_agent.authenticate()
        slack_agent.save()

        assert len(slack_app_request_factory.calls) == 1
        assert slack_app_request_factory.calls[0].request.method == 'POST'

        slack_team = slack_team_factory(slack_agent=slack_agent)
        topic_channel_id = slack_agent_factory.build().topic_channel_id

        mutation = f'''
          mutation {{
            updateSlackAgentTopicChannelAndActivate(input: {{slackTeamId: "{slack_team.id}",
                                                            topicChannelId: "{topic_channel_id}"}}) {{
              slackAgent {{
                topicChannelId
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['updateSlackAgentTopicChannelAndActivate'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_team(self, auth_client, slack_application_installation_factory, slack_agent_factory,
                                slack_team_factory, slack_app_request_factory):
        slack_agent = slack_agent_factory(topic_channel_id=None)
        slack_application_installation_factory(slack_agent=slack_agent)
        slack_agent.authenticate()
        slack_agent.save()

        assert len(slack_app_request_factory.calls) == 1
        assert slack_app_request_factory.calls[0].request.method == 'POST'

        slack_team = slack_team_factory.build(slack_agent=slack_agent)
        topic_channel_id = slack_agent_factory.build().topic_channel_id

        mutation = f'''
          mutation {{
            updateSlackAgentTopicChannelAndActivate(input: {{slackTeamId: "{slack_team.id}",
                                                            topicChannelId: "{topic_channel_id}"}}) {{
              slackAgent {{
                topicChannelId
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['updateSlackAgentTopicChannelAndActivate'] is None
        assert response.json()['errors'][0]['message'] == 'SlackAgent matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_slack_agent_status(self, auth_client, slack_agent_factory, slack_team_factory):
        slack_agent = slack_agent_factory(topic_channel_id=None)

        slack_team = slack_team_factory(slack_agent=slack_agent)
        topic_channel_id = slack_agent_factory.build().topic_channel_id

        mutation = f'''
          mutation {{
            updateSlackAgentTopicChannelAndActivate(input: {{slackTeamId: "{slack_team.id}",
                                                            topicChannelId: "{topic_channel_id}"}}) {{
              slackAgent {{
                topicChannelId
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['updateSlackAgentTopicChannelAndActivate'] is None
        assert response.json()['errors'][0]['message'] == "Can't switch from state 'INITIATED' using method 'activate'"

    @pytest.mark.django_db
    def test_valid(self, auth_client, slack_application_installation_factory, slack_agent_factory, slack_team_factory,
                   slack_app_request_factory):
        slack_agent = slack_agent_factory(topic_channel_id=None)
        slack_application_installation_factory(slack_agent=slack_agent)
        slack_agent.authenticate()
        slack_agent.save()

        assert len(slack_app_request_factory.calls) == 1
        assert slack_app_request_factory.calls[0].request.method == 'POST'

        slack_team = slack_team_factory(slack_agent=slack_agent)
        topic_channel_id = slack_agent_factory.build().topic_channel_id

        mutation = f'''
          mutation {{
            updateSlackAgentTopicChannelAndActivate(input: {{slackTeamId: "{slack_team.id}",
                                                            topicChannelId: "{topic_channel_id}"}}) {{
              slackAgent {{
                topicChannelId
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['updateSlackAgentTopicChannelAndActivate']['slackAgent'][
                   'topicChannelId'] == topic_channel_id
        assert response.json()['data']['updateSlackAgentTopicChannelAndActivate']['slackAgent']['status'] == 'ACTIVE'

        assert len(slack_app_request_factory.calls) == 2
        assert slack_app_request_factory.calls[1].request.method == 'PUT'
