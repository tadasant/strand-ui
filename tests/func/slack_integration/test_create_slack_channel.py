import pytest


class TestCreateSlackChannel:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_channel_factory, slack_team_factory, session_factory):
        session = session_factory()
        slack_team = slack_team_factory()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSlackChannel(input: {{id: "{slack_channel.id}", name: "{slack_channel.name}",
                                        slackTeamId: "{slack_team.id}", sessionId: {session.id}}}) {{
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_team(self, auth_client, slack_channel_factory, slack_team_factory, session_factory):
        session = session_factory()
        slack_team = slack_team_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSlackChannel(input: {{id: "{slack_channel.id}", name: "{slack_channel.name}",
                                        slackTeamId: "{slack_team.id}", sessionId: {session.id}}}) {{
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel'] is None
        assert response.json()['errors'][0]['message'] == f"{{'slack_team_id': ['Invalid pk \"{slack_team.id}\" - " \
                                                          "object does not exist.']}"

    @pytest.mark.django_db
    def test_invalid_session(self, auth_client, slack_channel_factory, slack_team_factory):
        slack_team = slack_team_factory()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSlackChannel(input: {{id: "{slack_channel.id}", name: "{slack_channel.name}",
                                        slackTeamId: "{slack_team.id}", sessionId: 0}}) {{
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel'] is None
        assert response.json()['errors'][0]['message'] == "{'session_id': ['Invalid pk \"0\" - " \
                                                          "object does not exist.']}"

    @pytest.mark.django_db
    def test_valid(self, auth_client, slack_channel_factory, slack_team_factory, session_factory):
        session = session_factory()
        slack_team = slack_team_factory()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSlackChannel(input: {{id: "{slack_channel.id}", name: "{slack_channel.name}",
                                        slackTeamId: "{slack_team.id}", sessionId: {session.id}}}) {{
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSlackChannel']['slackChannel']['name'] == slack_channel.name
