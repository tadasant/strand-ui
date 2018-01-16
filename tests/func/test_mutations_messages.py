import pytest

from app.messages.models import Message, Reply


class TestCreateMessage:

    @pytest.mark.django_db
    def test_create_message_unauthenticated(self, client, session_factory, user_factory, slack_event_factory,
                                            message_factory):
        session = session_factory()
        user = user_factory()
        slack_event = slack_event_factory()
        message = message_factory.build(session=session, author=user, slack_event=slack_event)

        mutation = f'''
          mutation {{
            createMessage(input: {{text: "{message.text}", sessionId: {session.id}, authorId: {user.id},
                                   time: "{message.time}", slackEventId: {slack_event.id}}}) {{
              message {{
                time
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createMessage'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_message(self, auth_client, session_factory, user_factory, slack_event_factory,
                            message_factory):
        session = session_factory()
        user = user_factory()
        slack_event = slack_event_factory()
        message = message_factory.build(session=session, author=user, slack_event=slack_event)

        mutation = f'''
          mutation {{
            createMessage(input: {{text: "{message.text}", sessionId: {session.id}, authorId: {user.id},
                                   time: "{message.time}", slackEventId: {slack_event.id}}}) {{
              message {{
                text
              }}
            }}
          }}        
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createMessage']['message']['text'] == message.text


class TestCreateReply:

    @pytest.mark.django_db
    def test_create_reply_unauthenticated(self, client, message_factory, user_factory, slack_event_factory,
                                          reply_factory):
        message = message_factory()
        user = user_factory()
        slack_event = slack_event_factory()
        reply = reply_factory.build(message=message, author=user, slack_event=slack_event)

        mutation = f'''
          mutation {{
            createReply(input: {{text: "{reply.text}", messageId: {message.id}, authorId: {user.id},
                                 time: "{reply.time}", slackEventId: {slack_event.id}}}) {{
              reply {{
                text
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.json()['data']['createReply'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_create_reply(self, auth_client, message_factory, user_factory, slack_event_factory, reply_factory):
        message = message_factory()
        user = user_factory()
        slack_event = slack_event_factory()
        reply = reply_factory.build(message=message, author=user, slack_event=slack_event)

        mutation = f'''
          mutation {{
            createReply(input: {{text: "{reply.text}", messageId: {message.id}, authorId: {user.id},
                                 time: "{reply.time}", slackEventId: {slack_event.id}}}) {{
              reply {{
                text
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.json()['data']['createReply']['reply']['text'] == reply.text
