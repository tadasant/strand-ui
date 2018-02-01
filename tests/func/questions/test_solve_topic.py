import pytest


class TestSolveTopic:

    @pytest.mark.django_db
    def test_unauthenticated(self, client, user_factory, topic_factory, session_factory):
        original_poster = user_factory()
        topic = topic_factory(original_poster=original_poster)
        session_factory(topic=topic)
        solver = user_factory()

        mutation = f'''
          mutation {{
            solveTopic(input: {{id: {topic.id},
                                   solverId: {solver.id}}}) {{
              topic {{
                session {{
                  timeEnd
                }}
                solver {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['solveTopic'] is None
        assert response.json()['errors'][0]['message'] == 'Unauthorized'

    @pytest.mark.django_db
    def test_invalid_topic(self, auth_client, user_factory, topic_factory, session_factory):
        original_poster = user_factory()
        topic = topic_factory(original_poster=original_poster)
        session_factory(topic=topic)
        solver = user_factory()

        mutation = f'''
          mutation {{
            solveTopic(input: {{id: 1,
                                   solverId: {solver.id}}}) {{
              topic {{
                session {{
                  timeEnd
                }}
                solver {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['solveTopic'] is None
        assert response.json()['errors'][0]['message'] == 'Topic matching query does not exist.'

    @pytest.mark.django_db
    def test_invalid_user(self, auth_client, user_factory, topic_factory, session_factory):
        original_poster = user_factory()
        topic = topic_factory(original_poster=original_poster)
        session_factory(topic=topic)

        mutation = f'''
          mutation {{
            solveTopic(input: {{id: {topic.id},
                                   solverId: 1}}) {{
              topic {{
                session {{
                  timeEnd
                }}
                solver {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['solveTopic'] is None
        assert response.json()['errors'][0]['message'] == 'User matching query does not exist.'

    @pytest.mark.django_db
    def test_valid(self, auth_client, user_factory, topic_factory, session_factory):
        original_poster = user_factory()
        topic = topic_factory(original_poster=original_poster)
        session_factory(topic=topic)
        solver = user_factory()

        mutation = f'''
          mutation {{
            solveTopic(input: {{id: {topic.id},
                                   solverId: {solver.id}}}) {{
              topic {{
                session {{
                  timeEnd
                }}
                solver {{
                  id
                }}
              }}
            }}
          }}
        '''
        response = auth_client.post('/graphql', {'query': mutation})

        assert response.status_code == 200
        assert response.json()['data']['solveTopic']['topic']['solver']['id'] == str(solver.id)
