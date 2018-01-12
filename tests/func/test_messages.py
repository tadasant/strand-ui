import graphene
import pytest

from app.messages.schema import Query


class TestMessageQuery():
    """Test message API queries"""

    @pytest.mark.django_db
    def test_get_message(self, message_factory):
        message = message_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              message(id: %s) {
                text
              }
            }
        ''' % message.id
        result = schema.execute(query)
        assert not result.errors
        assert result.data['message']['text'] == message.text

    @pytest.mark.django_db
    def test_get_messages(self, message_factory):
        message = message_factory()
        another_message = message_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
               messages {
                  text
               }
            }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert len(result.data['messages']) == 2


class TestReplyQuery():
    """Test reply API queries"""

    @pytest.mark.django_db
    def test_get_reply(self, reply_factory):
        reply = reply_factory()

        schema = graphene.Schema(query=Query)
        query = '''
            query {
              reply(id: %s) {
                message {
                  text
                }
              }
            }
        ''' % reply.id
        result = schema.execute(query)
        assert not result.errors
        assert result.data['reply']['message']['text'] == reply.message.text

    @pytest.mark.django_db
    def test_get_replies(self, reply_factory):
        reply = reply_factory()
        another_reply = reply_factory(message=reply.message)

        schema = graphene.Schema(query=Query)
        query = '''
            query {
               replies {
                 text
               }
            }
        '''
        result = schema.execute(query)
        assert not result.errors
        assert len(result.data['replies']) == 2