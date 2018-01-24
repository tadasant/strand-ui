import pytest


class TestCreateReplyFromSlack:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, session_factory, slack_channel_factory, slack_event_factory,
                             slack_user_factory, message_factory, reply_factory):
        session = session_factory()
        slack_channel = slack_channel_factory(session=session)
        message_slack_event = slack_event_factory()
        reply_slack_event = slack_event_factory()
        message_slack_user = slack_user_factory()
        reply_slack_user = slack_user_factory()
        message = message_factory(session=session, origin_slack_event=message_slack_event,
                                  author=message_slack_user.user)
        reply = reply_factory.build(message=message, origin_slack_event=reply_slack_event,
                                    author=reply_slack_user.user)

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}", time: "{reply.time}",
                                          messageOriginSlackEventTs: "{message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          originSlackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                message {{
                  author {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_slack_channel(self, auth_client, session_factory, slack_channel_factory, slack_event_factory,
                                   slack_user_factory, message_factory, reply_factory):
        session = session_factory()
        slack_channel = slack_channel_factory.build(session=session)
        message_slack_event = slack_event_factory()
        reply_slack_event = slack_event_factory()
        message_slack_user = slack_user_factory()
        reply_slack_user = slack_user_factory()
        message = message_factory(session=session, origin_slack_event=message_slack_event,
                                  author=message_slack_user.user)
        reply = reply_factory.build(message=message, origin_slack_event=reply_slack_event,
                                    author=reply_slack_user.user)

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}", time: "{reply.time}",
                                          messageOriginSlackEventTs: "{message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          originSlackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                message {{
                  author {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Message matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_slack_user(self, auth_client, session_factory, slack_channel_factory, slack_event_factory,
                                slack_user_factory, message_factory, reply_factory):
        session = session_factory()
        slack_channel = slack_channel_factory(session=session)
        message_slack_event = slack_event_factory()
        reply_slack_event = slack_event_factory()
        message_slack_user = slack_user_factory()
        reply_slack_user = slack_user_factory.build()
        message = message_factory(session=session, origin_slack_event=message_slack_event,
                                  author=message_slack_user.user)
        reply = reply_factory.build(message=message, origin_slack_event=reply_slack_event,
                                    author=reply_slack_user.user)

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}", time: "{reply.time}",
                                          messageOriginSlackEventTs: "{message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          originSlackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                message {{
                  author {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'User matching query does not exist.'

    @pytest.mark.django_db
    def test_create_invalid_message_slack_event(self, auth_client, session_factory, slack_channel_factory,
                                                slack_event_factory, slack_user_factory, message_factory,
                                                reply_factory):
        session = session_factory()
        slack_channel = slack_channel_factory(session=session)
        message_slack_event = slack_event_factory()
        wrong_message_slack_event = slack_event_factory()
        reply_slack_event = slack_event_factory()
        message_slack_user = slack_user_factory()
        reply_slack_user = slack_user_factory()
        message = message_factory(session=session, origin_slack_event=message_slack_event,
                                  author=message_slack_user.user)
        reply = reply_factory.build(message=message, origin_slack_event=reply_slack_event,
                                    author=reply_slack_user.user)

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}", time: "{reply.time}",
                                          messageOriginSlackEventTs: "{wrong_message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          originSlackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                message {{
                  author {{
                    id
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack'] is None
        assert response.json()['errors'][0]['message'] == 'Message matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, session_factory, slack_channel_factory,
                   slack_event_factory, slack_user_factory, message_factory,
                   reply_factory):
        session = session_factory()
        slack_channel = slack_channel_factory(session=session)
        message_slack_event = slack_event_factory()
        reply_slack_event = slack_event_factory()
        message_slack_user = slack_user_factory()
        reply_slack_user = slack_user_factory()
        message = message_factory(session=session, origin_slack_event=message_slack_event,
                                  author=message_slack_user.user)
        reply = reply_factory.build(message=message, origin_slack_event=reply_slack_event,
                                    author=reply_slack_user.user)

        mutation = f'''
          mutation {{
            createReplyFromSlack(input: {{text: "{reply.text}", time: "{reply.time}",
                                          messageOriginSlackEventTs: "{message_slack_event.ts}",
                                          slackChannelId: "{slack_channel.id}",
                                          slackUserId: "{reply_slack_user.id}",
                                          originSlackEventTs: "{reply_slack_event.ts}"}}) {{
              reply {{
                originSlackEvent {{
                  ts
                }}
                message {{
                  author {{
                    id
                  }}
                  session {{
                    participants {{
                      id
                    }}
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReplyFromSlack']['reply']['originSlackEvent']['ts'] == \
            reply_slack_event.ts
        assert response.json()['data']['createReplyFromSlack']['reply']['message']['author']['id'] == \
            str(message.author.id)
        assert {'id': str(reply_slack_user.user.id)} in response.json()['data']['createReplyFromSlack']['reply'][
            'message']['session']['participants']
