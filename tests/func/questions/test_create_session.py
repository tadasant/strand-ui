import pytest


class TestCreateSession:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, topic_factory, session_factory):
        topic = topic_factory()
        session = session_factory.build()

        mutation = f'''
          mutation {{
            createSession(input: {{timeStart: "{session.time_start}", timeEnd: "{session.time_end}",
                                   topicId: {topic.id}}}) {{
              session {{
                topic {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSession'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, topic_factory, session_factory):
        topic = topic_factory()
        session = session_factory.build()

        mutation = f'''
          mutation {{
            createSession(input: {{timeStart: "{session.time_start}", timeEnd: "{session.time_end}",
                                   topicId: {topic.id}}}) {{
              session {{
                topic {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createSession']['session']['topic']['id'] == str(topic.id)
