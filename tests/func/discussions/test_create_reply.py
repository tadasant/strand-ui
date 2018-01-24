import pytest


class TestCreateReply:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, message_factory, user_factory, reply_factory):
        message = message_factory()
        user = user_factory()
        reply = reply_factory.build(message=message, author=user)

        mutation = f'''
          mutation {{
            createReply(input: {{text: "{reply.text}", messageId: {message.id}, authorId: {user.id},
                                 time: "{reply.time}"}}) {{
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
    def test_valid(self, auth_client, message_factory, user_factory, reply_factory):
        message = message_factory()
        user = user_factory()
        reply = reply_factory.build(message=message, author=user)

        mutation = f'''
          mutation {{
            createReply(input: {{text: "{reply.text}", messageId: {message.id}, authorId: {user.id},
                                 time: "{reply.time}"}}) {{
              reply {{
                text
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.json()['data']['createReply']['reply']['text'] == reply.text
