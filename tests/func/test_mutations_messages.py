from datetime import datetime
import pytest


class TestMessageMutations():
    """Test message mutations"""

    @pytest.mark.django_db
    def test_create_message_unauthenticated(self, client, session_factory, user_factory, slack_event_factory):
        session = session_factory()
        user = user_factory()
        slack_event = slack_event_factory()
        time = datetime.now().isoformat()

        mutation = f'''
          mutation {{
            createMessage(input: {{text: "my message", sessionId: {session.id}, authorId: {user.id},
                                   time: "{time}", slackEventId: {slack_event.id}}}) {{
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