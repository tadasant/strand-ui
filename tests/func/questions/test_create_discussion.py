import pytest


class TestCreateDiscussion:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, topic_factory, discussion_factory):
        topic = topic_factory()
        discussion = discussion_factory.build()

        mutation = f'''
          mutation {{
            createDiscussion(input: {{timeStart: "{discussion.time_start}", timeEnd: "{discussion.time_end}",
                                   topicId: {topic.id}}}) {{
              discussion {{
                topic {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createDiscussion'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_valid(self, auth_client, topic_factory, discussion_factory):
        topic = topic_factory()
        discussion = discussion_factory.build()

        mutation = f'''
          mutation {{
            createDiscussion(input: {{timeStart: "{discussion.time_start}", timeEnd: "{discussion.time_end}",
                                   topicId: {topic.id}}}) {{
              discussion {{
                topic {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['createDiscussion']['discussion']['topic']['id'] == str(topic.id)
