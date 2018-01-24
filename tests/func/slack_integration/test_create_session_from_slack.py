import pytest


class TestCreateSessionFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, slack_channel_factory, slack_team_factory, session_factory,
                             question_factory):
        question = question_factory()
        slack_team = slack_team_factory()
        session = session_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSessionFromSlack(input: {{session: {{timeStart: "{session.time_start}",
                                                       questionId: {question.id}}},
                                                       id: "{slack_channel.id}",
                                                       name: "{slack_channel.name}",
                                                       slackTeamId: "{slack_team.id}"}}) {{
              session {{
                id
              }}
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSessionFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, slack_channel_factory, slack_team_factory, session_factory, question_factory):
        question = question_factory()
        slack_team = slack_team_factory()
        session = session_factory.build()
        slack_channel = slack_channel_factory.build()

        mutation = f'''
          mutation {{
            createSessionFromSlack(input: {{session: {{timeStart: "{session.time_start}",
                                                       questionId: {question.id}}},
                                                       id: "{slack_channel.id}",
                                                       name: "{slack_channel.name}",
                                                       slackTeamId: "{slack_team.id}"}}) {{
              session {{
                question {{
                  id
                }}
              }}
              slackChannel {{
                name
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSessionFromSlack']['session']['question']['id'] == str(question.id)
        assert response.json()['data']['createSessionFromSlack']['slackChannel']['name'] == slack_channel.name
