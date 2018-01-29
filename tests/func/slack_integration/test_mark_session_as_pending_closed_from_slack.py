import pytest


class TestMarkSessionAsPendingClosedFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, question_factory, session_factory, slack_channel_factory):
        question = question_factory()
        session = session_factory(question=question, status='STALE')
        slack_channel = slack_channel_factory(session=session)

        mutation = f'''
          mutation {{
            markSessionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              session {{
                status
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})
        print(response.content)
        assert response.status_code == 200
        assert response.json()['data']['markSessionAsPendingClosedFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, question_factory, session_factory, slack_channel_factory):
        question = question_factory()
        session = session_factory(question=question, status='STALE')
        slack_channel = slack_channel_factory.build(session=session)

        mutation = f'''
          mutation {{
            markSessionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              session {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['markSessionAsPendingClosedFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Session matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_session_state(self, auth_client, question_factory, session_factory, slack_channel_factory):
        question = question_factory()
        session = session_factory(question=question, status='OPEN')
        slack_channel = slack_channel_factory(session=session)

        mutation = f'''
          mutation {{
            markSessionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              session {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['markSessionAsPendingClosedFromSlack'] is None
        assert response.json()['errors'][0]['message'] == "Can't switch from state 'OPEN' using method " \
                                                          "'mark_as_pending_closed'"

    @pytest.mark.django_db
    def test_valid(self, auth_client, question_factory, session_factory, slack_channel_factory):
        question = question_factory()
        session = session_factory(question=question, status='STALE')
        slack_channel = slack_channel_factory(session=session)

        mutation = f'''
          mutation {{
            markSessionAsPendingClosedFromSlack(input: {{slackChannelId: "{slack_channel.id}"}}) {{
              session {{
                status
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['markSessionAsPendingClosedFromSlack']['session']['status'] == 'PENDING CLOSED'
