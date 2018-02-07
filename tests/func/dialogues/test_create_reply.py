import pytz
from datetime import datetime, timedelta

import pytest

from app.topics.models import Discussion


class TestCreateReply:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, message_factory, reply_factory):
        message = message_factory()
        reply = reply_factory.build(message=message)

        mutation = f'''
          mutation {{
            createReply(input: {{text: "{reply.text}", messageId: {message.id}, authorId: {message.author.id},
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
    def test_closed_discussion(self, auth_client, discussion_factory, message_factory, reply_factory):
        discussion = discussion_factory(status='CLOSED')
        message = message_factory(discussion=discussion)
        reply = reply_factory.build(message=message)

        mutation = f'''
          mutation {{
            createReply(input: {{text: "{reply.text}", messageId: {message.id}, authorId: {message.author.id},
                                 time: "{reply.time}"}}) {{
              reply {{
                text
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReply'] is None
        assert response.json()['errors'][0]['message'] == "{'non_field_errors': ['Cannot create reply to message in " \
                                                          "closed discussion']}"

    @pytest.mark.django_db
    def test_valid(self, auth_client, message_factory, reply_factory):
        message = message_factory()
        reply = reply_factory.build(message=message)

        mutation = f'''
          mutation {{
            createReply(input: {{text: "{reply.text}", messageId: {message.id}, authorId: {message.author.id},
                                 time: "{reply.time}"}}) {{
              reply {{
                text
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.json()['data']['createReply']['reply']['text'] == reply.text

    @pytest.mark.django_db()
    def test_marks_discussion_as_open(self, auth_client, discussion_factory, message_factory, reply_factory):
        discussion = discussion_factory()
        message = message_factory(time=datetime.now(tz=pytz.UTC) - timedelta(minutes=31), discussion=discussion)
        discussion.mark_as_stale()
        discussion.save()

        reply = reply_factory.build(message=message)

        mutation = f'''
          mutation {{
            createReply(input: {{text: "{reply.text}", messageId: {reply.message.id}, authorId: {message.author.id},
                                 time: "{reply.time}"}}) {{
              reply {{
                text
                message {{
                  discussion {{
                    status
                  }}
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createReply']['reply']['text'] == reply.text
        assert response.json()['data']['createReply']['reply']['message']['discussion']['status'] == 'OPEN'
