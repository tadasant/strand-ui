import pytest


class TestCreateMessageFromSlack:
    @pytest.mark.django_db
    def test_unauthenticated(self, client, session_factory, slack_channel_factory, user_factory, slack_user_factory,
                             slack_event_factory, message_factory):
        session = session_factory()
        slack_channel = slack_channel_factory(session=session)
        user = user_factory()
        slack_user = slack_user_factory(user=user)

        slack_event = slack_event_factory.build()
        message = message_factory.build()

        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}",
                                            slackChannelId: "{slack_channel.id}", slackUserId: "{slack_user.id}",
                                            originSlackEventTs: "{slack_event.ts}"}}) {{
              message {{
                text
                originSlackEvent {{
                  ts
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, session_factory, slack_channel_factory, user_factory,
                                slack_user_factory, slack_event_factory, message_factory):
        session = session_factory()
        slack_channel = slack_channel_factory(session=session)
        user = user_factory()
        slack_user = slack_user_factory.build(user=user)

        slack_event = slack_event_factory.build()
        message = message_factory.build()

        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}",
                                            slackChannelId: "{slack_channel.id}", slackUserId: "{slack_user.id}",
                                            originSlackEventTs: "{slack_event.ts}"}}) {{
              message {{
                text
                originSlackEvent {{
                  ts
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'User matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, session_factory, slack_channel_factory, user_factory,
                                   slack_user_factory, slack_event_factory, message_factory):
        session = session_factory()
        slack_channel = slack_channel_factory.build(session=session)
        user = user_factory()
        slack_user = slack_user_factory(user=user)

        slack_event = slack_event_factory.build()
        message = message_factory.build()

        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}",
                                            slackChannelId: "{slack_channel.id}", slackUserId: "{slack_user.id}",
                                            originSlackEventTs: "{slack_event.ts}"}}) {{
              message {{
                text
                originSlackEvent {{
                  ts
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createMessageFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Session matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, session_factory, slack_channel_factory, user_factory,
                   slack_user_factory, slack_event_factory, message_factory):
        session = session_factory()
        slack_channel = slack_channel_factory(session=session)
        user = user_factory()
        slack_user = slack_user_factory(user=user)

        slack_event = slack_event_factory.build()
        message = message_factory.build()

        mutation = f'''
          mutation {{
            createMessageFromSlack(input: {{text: "{message.text}",
                                            slackChannelId: "{slack_channel.id}", slackUserId: "{slack_user.id}",
                                            originSlackEventTs: "{slack_event.ts}"}}) {{
              message {{
                author {{
                  id
                }}
                originSlackEvent {{
                  ts
                }}
                session {{
                  id
                  participants {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createMessageFromSlack']['message']['author']['id'] == \
            str(slack_user.user.id)
        assert response.json()['data']['createMessageFromSlack']['message']['session']['id'] == str(session.id)
        assert response.json()['data']['createMessageFromSlack']['message']['originSlackEvent']['ts'] == \
            str(slack_event.ts)
        assert {'id': str(user.id)} in response.json()['data']['createMessageFromSlack']['message']['session'][
            'participants']
