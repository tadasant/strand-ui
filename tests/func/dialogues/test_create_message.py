import pytest


class TestCreateMessage:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, discussion_factory, user_factory, message_factory):
        discussion = discussion_factory()
        user = user_factory()
        message = message_factory.build(discussion=discussion, author=user)

        mutation = f'''
          mutation {{
            createMessage(input: {{text: "{message.text}", discussionId: {discussion.id}, authorId: {user.id},
                                   time: "{message.time}"}}) {{
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
    def test_valid(self, auth_client, discussion_factory, user_factory, message_factory):
        discussion = discussion_factory()
        user = user_factory()
        message = message_factory.build(discussion=discussion, author=user)

        mutation = f'''
          mutation {{
            createMessage(input: {{text: "{message.text}", discussionId: {discussion.id}, authorId: {user.id},
                                   time: "{message.time}"}}) {{
              message {{
                text
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createMessage']['message']['text'] == message.text
